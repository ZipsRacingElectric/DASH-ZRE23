# Libraries
import os
import can

import threading
from threading import Thread

# Imports
from can_interface import CanInterface

class Main(CanInterface):
    def __init__(self, database, messageHandler=None):
        print("CAN - Using Innomaker USB-CAN Library")
        print("CAN - Platform: Linux")

        super().__init__(database, messageHandler)
        self.channels = []

    def OpenChannel(self, bitrate, id):
        if(id < 0 or id >= len(self.channels)): return
        self.channels.append(OpenChannel(id, bitrate=bitrate))

    def CloseChannel(self, id):
        CloseChannel(id)

    def Scan(self, index):
        while(self.online):
            message = self.channels[index].recv(10.0)
            if(message != None):
                self.Receive(message.arbitration_id, message.data)
        self.CloseChannel(index)

    def Transmit(self, id, data, channel):
        if(channel < 0 or channel > len(self.channels)-1): return
        canFrame = can.Message(arbitration_id=id, data=data, is_extended_id=False)
        self.channels[channel].send(canFrame)
        self.Receive(id, data)

    def Begin(self):
        self.online = True
        
        for index in range(len(self.channels)):
            channelThread = Thread(target= lambda: self.Scan(index))
            channelThread.start()

    def Kill(self):
        print("CAN - Terminating...")
        self.online = False

def OpenChannel(id, bitrate):
    print(f"CAN - Channel {id} Opening...")

    os.system(f'sudo ifconfig can{id} down')
    os.system(f'sudo ip link set can{id} type can bitrate {bitrate}')
    os.system(f'sudo ifconfig can{id} txqueuelen 100000')
    os.system(f'sudo ifconfig can{id} up')

    return can.interface.Bus(channel = f'can{id}', bustype = 'socketcan')

def CloseChannel(id):
    print(f"CAN - Closing Channel {id}")

    os.system(f'sudo ifconfig can{id} down')