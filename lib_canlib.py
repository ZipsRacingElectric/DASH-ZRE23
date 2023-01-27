# Libraries
import sys

import threading
from threading import Thread

import canlib
from canlib import canlib
from canlib import Frame
from canlib.canlib import ChannelData

# Imports
from appCan import CanInterface

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

class Main(CanInterface):
    def __init__(self, database, channelBitrates=[None], messageHandler=None):
        print("CAN - Using Kvaser Canlib Library")
        super().__init__(database, channelBitrates, messageHandler)

        # Platform Identification
        if(sys.platform == 'win32'):
            print("CAN - Platform: Windows 32-Bit")
            print("CAN - Canlib Version:", canlib.dllversion())
            return # Complete Setup
        if(sys.platform == 'linux'):
            print("CAN - Platform: Linux")
            print("CAN - Linux Canlib not Supported")
            return # Incomplete Setup
        print("CAN - Unidentified System Platform.")
        return # Incomplete Setup

    def OpenChannel(self, bitrate, id):
        self.channels.append(OpenChannel(id, bitrate=CanlibBitrate[bitrate]))

    def CloseChannel(self, channel):
        CloseChannel(channel)

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
        self.online = True

        for index in range(len(self.channels)):
            print("CAN - Channel", index, "Thread Starting...")
            if(self.channels[index] == None): continue
            channelThread = Thread(target= lambda: self.Scan(self.channels[index]))
            channelThread.start()
            print("CAN - Channel", index, "Thread Started.")

    def Kill(self):
        print("CAN - Terminating...")
        self.online = False

def OpenChannel(channelId, openFlags=canlib.canOPEN_ACCEPT_VIRTUAL, bitrate=canlib.canBITRATE_500K, bitrateFlags=canlib.canDRIVER_NORMAL):
    channel = canlib.openChannel(channelId, openFlags)
    print("CAN - Device:", ChannelData(channelId).channel_name, "- ID:", ChannelData(channelId).card_upc_no)
    channel.setBusOutputControl(bitrateFlags)
    channel.setBusParams(bitrate)
    channel.busOn()
    return channel

def CloseChannel(channel):
    print("CAN - Device Closed:", ChannelData(channel.index).channel_name)
    channel.busOff()
    channel.close()

# class Canlib():
#     def __init__(self, bitrate0=None, bitrate1=None, messageHandler=None):
#         print("CAN - Using Kvaser Canlib Library")
#         self.messageHandler = messageHandler

#         # Open Channel 0
#         if(bitrate0 != None):
#             self.can0 = OpenChannel(0, bitrate=CanlibBitrate[bitrate0])
#             print("CAN - Opened Channel 0. Bitrate:", bitrate0)
#         else:
#             self.can0 = None

#         # Open Channel 1
#         if(bitrate1 != None):
#             self.can1 = OpenChannel(1, bitrate=CanlibBitrate[bitrate1])
#             print("CAN - Opened Channel 1. Bitrate:", bitrate1)
#         else:
#             self.can1 = None

#         # Platform Identification
#         if(sys.platform == 'win32'):
#             print("CAN - Platform: Windows 32-Bit")
#             print("CAN - Canlib Version:", canlib.dllversion())
#             return # Complete Setup
#         if(sys.platform == 'linux'):
#             print("CAN - Platform: Linux")
#             print("CAN - Linux Canlib not Supported")
#             return # Incomplete Setup
#         print("CAN - Unidentified System Platform.")
#         return # Incomplete Setup

#     def Update(self):
#         # Read Channel 0
#         if(self.can0 != None):
#             try:
#                 frame = self.can0.read()
#                 if(self.messageHandler != None):
#                     self.messageHandler(frame.id, frame.data)
#             except (canlib.canNoMsg) as ex:
#                 pass # No Message
#             except (canlib.canError) as ex:
#                 # Error Frame
#                 print("CAN - Error:", ex)
        
#         # # Read Channel 1
#         # if(self.can1 != None):
#         #     try:
#         #         frame = self.can1.read()
#         #         if(self.messageHandler != None):
#         #             self.messageHandler(frame.id, frame.data)
#         #     except (canlib.canNoMsg) as ex:
#         #         pass # No Message
#         #     except (canlib.canError) as ex:
#         #         # Error Frame
#         #         print("CAN - Error:", ex)

#     def Kill(self):
#         if(self.can0 != None):
#             CloseChannel(self.can0)
#             self.can0 = None
#         if(self.can1 != None):
#             CloseChannel(self.can1)
#             self.can1 = None

#     def Send(self, messageId, messageData, channel):
#         print("CAN - Sending Message:", hex(messageId), " Data:", messageData)
#         messageFrame = Frame(messageId, messageData, len(messageData), canlib.MessageFlag.STD)
#         if(channel == 0 and self.can0 != None): self.can0.write(messageFrame)
#         if(channel == 1 and self.can1 != None): self.can1.write(messageFrame)