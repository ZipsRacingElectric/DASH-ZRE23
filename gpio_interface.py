# GPIO Interface --------------------------------------------------------------------------------------------------------------
# Author: Cole Barach
# Date Created: 23.04.05
# Date Updated: 23.04.05

# Libraries -------------------------------------------------------------------------------------------------------------------
import gpiozero

import os
import sys
import threading
import time

import logging

# Imports ---------------------------------------------------------------------------------------------------------------------
import config

import can_interface

# Functions -------------------------------------------------------------------------------------------------------------------
def Setup(database, can_transceiver):
    if(sys.platform == "win32"): return None

    interface = Main()

    interface.InsertInterrupt(config.GPIO_START_BUTTON, lambda: StartButtonPress(can_transceiver))
    
    return interface

def StartButtonPress(can_transceiver):
    can_interface.SendCommandDriveStart(can_transceiver, True)

# GUI Object ------------------------------------------------------------------------------------------------------------------
class Main():
    def __init__(self, title, database, framerate=0):
        try:
            logging.debug("GPIO - Initializing...")
        
            self.inputs      = dict()
            self.interrupts  = dict()
            self.inputStates = dict()
            self.threads     = []

            self.online = True

            logging.debug("GPIO - Initialized.")
        except:
            logging.error("GPIO Initialization failed.")

    def InsertInterrupt(self, pin, handler):
        self.interrupts[pin] = handler

        self.inputs[pin] = gpiozero.Button(pin)
        
        self.threads.append(threading.Thread(target=lambda: self.ScanInterrupt(pin)))
        
    def ScanInterrupt(self, pin):
        while(self.online):
            if(self.inputs[pin].is_pressed and not self.inputStates[pin]):
                self.interrupts[pin]

            self.inputStates[pin] = self.inputs[pin].is_pressed

            time.sleep(config.GPIO_TIME_PERIOD)

    def Kill(self):
        self.online = False