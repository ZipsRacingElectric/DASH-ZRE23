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
    try:
        if(sys.platform == "win32"): return None

        interface = Main()

        interface.InsertInterrupt(config.GPIO_BUTTON_START, lambda: StartButtonPress(can_transceiver))
        
        return interface
    except Exception as e:
        logging.error("GPIO Setup failure: " + str(e))
        raise

def StartButtonPress(can_transceiver):
    can_interface.SendCommandDriveStart(can_transceiver, True)

# GUI Object ------------------------------------------------------------------------------------------------------------------
class Main():
    def __init__(self):
        try:
            logging.debug("GPIO - Initializing...")
        
            self.inputs      = dict()
            self.interrupts  = dict()
            self.inputStates = dict()

            self.online = True

            logging.debug("GPIO - Initialized.")
        except Exception as e:
            logging.error("GPIO Initialization failed: " + str(e))

    def Begin(self):
        self.scanningThread = threading.Thread(target=self.ScanInterrupts)
        self.scanningThread.start()

    def InsertInterrupt(self, pin, handler):
        try:
            logging.debug(f"GPIO - Inserting Interrupt for Pin: {pin}...")
            self.interrupts[pin] = handler

            self.inputs[pin] = gpiozero.Button(pin)
        except Exception as e:
            logging.error("GPIO interrupt insertion failure:  " + str(e))
            pass
        
    def ScanInterrupts(self):
        try:
            while(self.online):
                for pin, input in self.inputs:
                    logging.debug(f"GPIO - Pin {pin} Reading: " + str(input.is_pressed))
                    
                    if(input.is_pressed and not self.inputStates[pin]): self.interrupts[pin]()

                    self.inputStates[pin] = input.is_pressed

                    time.sleep(config.GPIO_TIME_PERIOD)
        except Exception as e:
            logging.error("Interrupt scan error: " + str(e))
            pass

    def Kill(self):
        self.online = False