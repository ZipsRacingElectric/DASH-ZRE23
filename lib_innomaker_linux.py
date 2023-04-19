# Innomaker USB-CAN Linux Library ---------------------------------------------------------------------------------------------
# Author: Cole Barach
# Date Created: 23.01.23
# Date Updated: 23.01.30
#   This module provides a standard interface for the Innomaker USB-CAN library. The Main object of this script is a
#   CAN Interface object which provides members for Transmitting and Receiving Messages.

# Libraries -------------------------------------------------------------------------------------------------------------------
import can

import os

import threading
from threading import Thread

import logging

# Imports ---------------------------------------------------------------------------------------------------------------------
import can_interface
from can_interface import CanInterface

# Objects ---------------------------------------------------------------------------------------------------------------------
class Main(CanInterface):
    def __init__(self, database, messageHandler=None, timingFunction=None, timingPeriod=None):
        print("CAN - Using Innomaker USB-CAN Library")
        print("CAN - Platform: Linux")

        super().__init__(database, messageHandler, timingFunction, timingPeriod)
        self.channels = []

    def OpenChannel(self, bitrate, id):
        if(id < 0): return
        self.channels.append(OpenChannel(id, bitrate=bitrate))

    def CloseChannel(self, id):
        CloseChannel(id)

    def Scan(self, index):
        try:
            while(self.online):
                message = self.channels[index].recv(10.0)
                if(message != None):
                    self.Receive(message.arbitration_id, message.data)
            self.CloseChannel(index)
        except Exception as e:
            logging.error("Innomaker CAN Scanning Failure. " + str(e))

    def Transmit(self, id, data, channel):
        if(channel < 0 or channel > len(self.channels)-1): return
        canFrame = can.Message(arbitration_id=id, data=data, is_extended_id=False)
        self.channels[channel].send(canFrame)
        self.Receive(id, data)

    def Begin(self):
        try:
            super().Begin()
            
            for index in range(len(self.channels)):
                print(f"CAN - Channel {index} Thread Starting...")
                channelThread = Thread(target= lambda: self.Scan(index))
                channelThread.start()
                print(f"CAN - Channel {index} Thread Started.")
        except Exception as e:
            logging.error("Could not begin CAN process: " + str(e))
            raise

# Functions -------------------------------------------------------------------------------------------------------------------
def OpenChannel(id, bitrate):
    print(f"CAN - Channel {id} Opening...")

    os.system(f'sudo ifconfig can{id} down')
    os.system(f'sudo ip link set can{id} type can bitrate {bitrate}')
    os.system(f'sudo ifconfig can{id} txqueuelen 100000')
    os.system(f'sudo ifconfig can{id} up')

    return can.interface.Bus(channel = f'can{id}', bustype = 'socketcan')

def CloseChannel(id):
    print(f"CAN - Closing Channel {id}")

    os.system(f'ifconfig can{id} down')