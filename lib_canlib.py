# CANLIB Library --------------------------------------------------------------------------------------------------------------
# Author: Cole Barach
# Date Created: 22.11.29
# Date Updated: 23.01.30
#   This module provides a standard interface for the KVaser CANLIB library. The Main object of this script is a CAN Interface
#   object which provides members for Transmitting and Receiving Messages.

# Libraries -------------------------------------------------------------------------------------------------------------------
import canlib
from canlib import canlib
from canlib import Frame
from canlib.canlib import ChannelData

import threading
from threading import Thread

# Imports ---------------------------------------------------------------------------------------------------------------------
import can_interface
from can_interface import CanInterface

import log
from log import print

# Enumarables -----------------------------------------------------------------------------------------------------------------
CanlibBitrate = {
    10000   : canlib.canBITRATE_10K,
    50000   : canlib.canBITRATE_50K,
    62000   : canlib.canBITRATE_62K,
    83000   : canlib.canBITRATE_83K,
    100000  : canlib.canBITRATE_100K,
    125000  : canlib.canBITRATE_125K,
    250000  : canlib.canBITRATE_250K,
    1000000 : canlib.canBITRATE_1M
}

# Objects ---------------------------------------------------------------------------------------------------------------------
class Main(CanInterface):
    def __init__(self, database, messageHandler=None, timingFunction=None, timingPeriod=None):
        print("CAN - Using Kvaser Canlib Library")
        print("CAN - Canlib Version:" + str(canlib.dllversion()))
        super().__init__(database, messageHandler, timingFunction, timingPeriod)

    def OpenChannel(self, bitrate, id):
        self.channels.append(OpenChannel(id, bitrate=CanlibBitrate[bitrate]))

    def CloseChannel(self, channel):
        CloseChannel(channel)

    def Transmit(self, id, data, channelId):
        frame = Frame(id_=id, data=data, flags=canlib.MessageFlag.STD )
        self.channels[channelId].write(frame)
        self.Receive(id, data)

    def Scan(self, channel):
        while(self.online):
            try:
                frame = channel.read()
                if(self.messageHandler != None): self.messageHandler(self.database, frame.id, frame.data)
            except (canlib.canNoMsg) as ex:
                pass # No Message
            except (canlib.canError) as ex:
                # Error Frame
                print("CAN - Error:", ex)

    def Begin(self):
        super().Begin()

        for index in range(len(self.channels)):
            print(f"CAN - Channel {index} Thread Starting...")
            if(self.channels[index] == None): continue
            channelThread = Thread(target= lambda: self.Scan(self.channels[index]))
            channelThread.start()
            print(f"CAN - Channel {index} Thread Started.")

# Functions -------------------------------------------------------------------------------------------------------------------
def OpenChannel(channelId, openFlags=canlib.canOPEN_ACCEPT_VIRTUAL, bitrate=canlib.canBITRATE_500K, bitrateFlags=canlib.canDRIVER_NORMAL):
    channel = canlib.openChannel(channelId, openFlags)
    print("CAN - Device: " + ChannelData(channelId).channel_name + " - ID:" + str(ChannelData(channelId).card_upc_no))
    channel.setBusOutputControl(bitrateFlags)
    channel.setBusParams(bitrate)
    channel.busOn()
    return channel

def CloseChannel(channel):
    print("CAN - Device Closed:" + ChannelData(channel.index).channel_name)
    channel.busOff()
    channel.close()