# Innomaker USB-CAN Windows Library -------------------------------------------------------------------------------------------
# Author: Cole Barach
# Date Created: 23.01.23
# Date Updated: 23.01.30
#   This module provides a standard interface for the Innomaker USB-CAN library. The Main object of this script is a
#   CAN Interface object which provides members for Transmitting and Receiving Messages.

# Libraries -------------------------------------------------------------------------------------------------------------------
from gs_usb.gs_usb import GsUsb
from gs_usb.gs_usb_frame import GsUsbFrame
from gs_usb.constants import CAN_EFF_FLAG
from gs_usb.constants import CAN_ERR_FLAG
from gs_usb.constants import CAN_RTR_FLAG
from gs_usb.gs_usb import GS_CAN_MODE_NORMAL
from gs_usb.gs_usb import GS_CAN_MODE_LISTEN_ONLY
from gs_usb.gs_usb import GS_CAN_MODE_LOOP_BACK
from gs_usb.gs_usb import GS_CAN_MODE_ONE_SHOT

import threading
from threading import Thread

# Imports ---------------------------------------------------------------------------------------------------------------------
import can_interface
from can_interface import CanInterface

# Objects ---------------------------------------------------------------------------------------------------------------------
class Main(CanInterface):
    def __init__(self, database, messageHandler=None, timingFunction=None, timingPeriod=None):
        super().__init__(database, messageHandler, timingFunction, timingPeriod)

        print("CAN - Using Innomaker USB-CAN Library")
        print("CAN - Platform: Windows")

        self.channels = GsUsb.scan()

        if len(self.channels) == 0:
            print("CAN - No GS-USB Devices Found.")
            return

        self.channels[0].stop()

    def OpenChannel(self, bitrate, id):
        if(id < 0 or id >= len(self.channels)): return
        OpenChannel(bitrate, self.channels[id])

    def CloseChannel(self, id):
        CloseChannel(self.channels[id])

    def Scan(self, index):
        frame = GsUsbFrame()
        while(self.online):
            self.channels[index].read(frame, 1)
            if(frame.can_id & CAN_ERR_FLAG != CAN_EFF_FLAG):
                self.messageHandler(self.database, frame.arbitration_id, frame.data)
        self.CloseChannel(index)

    def Transmit(self, id, data, channel):
        if(channel < 0 or channel > len(self.channels)-1): return
        messageFrame = GsUsbFrame(can_id=id, data=data)

        self.channels[channel].send(messageFrame)
        self.Receive(id, data)

    def Begin(self):
        super().Begin()
        
        for index in range(len(self.channels)):
            print(f"CAN - Channel {index} Thread Starting...")
            channelThread = Thread(target= lambda: self.Scan(index))
            channelThread.start()
            print(f"CAN - Channel {index} Thread Started.")

# Functions -------------------------------------------------------------------------------------------------------------------
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