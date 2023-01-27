# Libraries
import sys

import os
import can

import threading
from threading import Thread

# Imports
from can_interface import CanInterface

class Main(CanInterface):
    def __init__(self, database, channelBitrates=[None], messageHandler=None):
        if(sys.platform == "win32"): return
        print("CAN - Using Innomaker USB-CAN Library")
        super().__init__(database, channelBitrates, messageHandler)

        os.system('sudo ifconfig can0 down')
        os.system('sudo ip link set can0 type can bitrate ' + str(channelBitrates[0]))
        os.system('sudo ifconfig can0 txqueuelen 100000')
        os.system('sudo ifconfig can0 up')

        self.can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')

    # def OpenChannel(self, bitrate, id):
    #     self.channels.append(OpenChannel(id, bitrate=CanlibBitrate[bitrate]))

    # def CloseChannel(self, channel):
    #     CloseChannel(channel)

    def Scan(self):
        while(self.online):
            message = self.can0.recv(10.0)
            if(message != None):
                self.messageHandler(self.database, message.arbitration_id, message.data)

    def Begin(self):
        self.online = True
        print("CAN - Channel", 0, "Thread Starting...")
        channelThread = Thread(target= lambda: self.Scan())
        channelThread.start()

    def Kill(self):
        print("CAN - Terminating...")
        self.online = False