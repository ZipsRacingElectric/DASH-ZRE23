# Libraries
from gs_usb.gs_usb import GsUsb
from gs_usb.gs_usb_frame import GsUsbFrame
from gs_usb.constants import CAN_EFF_FLAG
from gs_usb.constants import CAN_ERR_FLAG
from gs_usb.constants import CAN_RTR_FLAG
from gs_usb.gs_usb import GS_CAN_MODE_NORMAL
from gs_usb.gs_usb import GS_CAN_MODE_LISTEN_ONLY
from gs_usb.gs_usb import GS_CAN_MODE_LOOP_BACK
from gs_usb.gs_usb import GS_CAN_MODE_ONE_SHOT

import time

import threading
from threading import Thread

# Imports
from can_interface import CanInterface

class Main(CanInterface):
    def __init__(self, database, messageHandler=None):
        print("CAN - Using Innomaker USB-CAN Library")
        print("CAN - Platform: Windows")

        super().__init__(database, messageHandler)
        self.channels = GsUsb.scan()

        if len(self.channels) == 0:
            print("CAN - No GS-USB Devices Found.")
            return

        self.channels[0].stop()
            
    def OpenChannel(self, bitrate, id):
        OpenChannel(bitrate, self.channels[id])

    def CloseChannel(self, id):
        CloseChannel(self.channels[id])

    def Scan(self, index):
        inFrame = GsUsbFrame()
        while(self.online):
            self.channels[index].read(inFrame, 1)
            if(inFrame.can_id & CAN_ERR_FLAG != CAN_EFF_FLAG):
                self.messageHandler(self.database, inFrame.arbitration_id, inFrame.data)
        self.CloseChannel(index)

    def Send(self, id, data, channel):
        if(channel < 0 or channel > len(self.channels)-1): return
        messageFrame = GsUsbFrame(can_id=id, data=data)

        self.channels[channel].send(messageFrame)

    def Begin(self):
        self.online = True
        
        for index in range(len(self.channels)):
            channelThread = Thread(target= lambda: self.Scan(index))
            channelThread.start()

    def Kill(self):
        print("CAN - Terminating...")
        self.online = False

def OpenChannel(bitrate, channel):
    print(f"CAN - Channel {channel.address} Opening...")

    success = channel.set_bitrate(bitrate)

    if(not success):
        print(f"CAN - Failed to Open Channel {channel.address} at Bitrate {bitrate}.")
        return

    channel.start(GS_CAN_MODE_LOOP_BACK)

def CloseChannel(channel):
    print(f"CAN - Closing Channel {channel.address}")

    channel.stop()