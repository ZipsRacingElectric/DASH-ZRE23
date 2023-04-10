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
def Setup(db, canT):
    try:
        global database
        global can_transmitter
        database = db
        can_transmitter = canT

        if(sys.platform == "win32"): return None

        interface = Main()

        interface.InsertDigital(config.GPIO_BUTTON_START, lambda: StartButtonPress(can_transmitter))
        
        interface.InsertRotary(config.GPIO_ROT_TORQUE_PIN_A, config.GPIO_ROT_TORQUE_PIN_B, TorqueEncoderInterrupt)
        interface.InsertRotary(config.GPIO_ROT_REGEN_PIN_A,  config.GPIO_ROT_REGEN_PIN_B,  TorqueEncoderInterrupt)

        interface.InsertService(CanSendService)

        return interface
    except Exception as e:
        logging.error("GPIO Setup failure: " + str(e))
        raise

def StartButtonPress(can_transceiver):
    can_interface.SendCommandDriveStart(can_transceiver, True)

def TorqueEncoderInterrupt(direction):
    global database
    database["Torque_Limit"] += direction * config.GPIO_ROT_TORQUE_SENSITIVITY

def RegenEncoderInterrupt(direction):
    global database
    database["Torque_Limit_Regen"] += direction * config.GPIO_ROT_REGEN_SENSITIVITY

def CanSendService():
    global can_transmitter
    can_interface.SendCommandDriveConfiguration(can_transmitter)

# GUI Object ------------------------------------------------------------------------------------------------------------------
class Main():
    def __init__(self):
        try:
            logging.debug("GPIO - Initializing...")
        
            self.digitalInputs     = dict()
            self.rotaryInputs      = dict()
            self.digitalStates     = dict()
            self.rotaryStates      = dict()
            self.digitalInterrupts = dict()
            self.rotaryInterrupts  = dict()
            self.services          = []

            self.online = True

            logging.debug("GPIO - Initialized.")
        except Exception as e:
            logging.error("GPIO Initialization failed: " + str(e))

    def Begin(self):
        self.scanningThread = threading.Thread(target=self.ScanInterrupts)
        self.scanningThread.start()

    def InsertDigital(self, pin, handler):
        try:
            logging.debug(f"GPIO - Inserting Digital Interrupt for Pin: {pin}...")
            self.digitalInputs[pin]     = gpiozero.Button(pin)
            self.digitalStates[pin]     = False
            self.digitalInterrupts[pin] = handler
        except Exception as e:
            logging.error("GPIO Digital Interrupt Insertion Failed: " + str(e))
            pass

    def InsertRotary(self, pinA, pinB, handler):
        try:
            logging.debug(f"GPIO - Inserting Rotary Interrupt for Pins: {pinA}, {pinB}...")
            self.rotaryInputs[pinA]     = (gpiozero.Button(pinA), gpiozero.Button(pinB))
            self.rotaryStates[pinA]     = False
            self.rotaryInterrupts[pinA] = handler
        except Exception as e:
            logging.error("GPIO Rotary Interrupt Insertion Failed: " + str(e))
            pass

    def InsertService(self, service):
        self.services.append(service)
        
    def ScanInterrupts(self):
        try:
            while(self.online):
                # Digital Inputs
                for pin, input in self.digitalInputs.items():
                    if(input.is_pressed and not self.digitalStates[pin]):
                        logging.debug(f"GPIO - Pin {str(pin)} Interrupt Called.")
                        self.interrupts[pin]()

                    self.digitalStates[pin] = input.is_pressed

                # Rotary Inputs
                for pin, input in self.rotaryInputs.items():
                    if(not self.rotaryStates[pin] and input[0].is_pressed): # Rising Edge
                        if(input[1].is_pressed):
                            # A is Rising and B is High (Forwards)
                            self.rotaryInterrupts[pin](1)
                        else:
                            # A is Rising and B is Low (Backwards)
                            self.rotaryInterrupts[pin](-1)

                    self.rotaryStates[pin] = input[0].is_pressed

                for service in self.services:
                    service()

                time.sleep(config.GPIO_TIME_PERIOD)
        except Exception as e:
            logging.error("Interrupt scan error: " + str(e))
            pass

    def Kill(self):
        self.online = False