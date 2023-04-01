# GUI Calibrarion View --------------------------------------------------------------------------------------------------------
# Author: Cole Barach
# Date Created: 22.10.14
# Date Updated: 23.01.30
#   This module contains all objects related to the Calibrarion View of the GUI. The View object may be instanced to create a
#   display capable of performing APPS and Brake calibrarion.

# Libraries -------------------------------------------------------------------------------------------------------------------
import lib_tkinter
from lib_tkinter import Orientation

import enum
from enum import Enum

# Includes --------------------------------------------------------------------------------------------------------------------
import gui
import config
import database
import can_interface

# Enumarables -----------------------------------------------------------------------------------------------------------------
class CalibrationState(Enum): # State of Calibration
    START                = 0, # - Buffer menu to avoid accidental calibration
    REQUEST_BOTH_MIN     = 1, # - For minimum values, tells the driver to not touch pedals
    REQUEST_APPS_MAX     = 2, # - For APPS Maximum values, tells the driver to press the throttle
    REQUEST_BRAKE_MAX    = 3, # - For Brake Maximum values, tells the driver to press the brake 
    FINISHED             = 4, # - For Valid Calibration Only
    FAILED               = 5  # - For Invalid Calibration

# Objects ---------------------------------------------------------------------------------------------------------------------
class View(gui.View):
    def __init__(self, parent, id, style, databaseObj, canTransmitter):
        # Root --------------------------------------------------------------------------------------------------------------------------------------
        super().__init__(parent, id, style, databaseObj)
        self.canTransmitter = canTransmitter

        # Root Partitioning -------------------------------------------------------------------------------------------------------------------------
        shortcutCommands = [lambda: self.parent.CloseViews(),
                            lambda: self.InputInterrupt(database.InputTypes.BUTTON_WHEEL_RIGHT),
                            lambda: self.InputInterrupt(database.InputTypes.BUTTON_WHEEL_LEFT),
                            0]
        shortcutLabels   = ["Back", 
                            "Next",
                            "Reset",
                            ""]
        
        self.root.columnconfigure(index=0, weight=1)
        self.root.rowconfigure(   index=0, weight=1)
        self.root.rowconfigure(   index=1, weight=0)

        # Root Widgets ------------------------------------------------------------------------------------------------------------------------------
        self.message   = lib_tkinter.GetLabel    (self.root, column=0, row=0, style=style, sticky="EW")
        self.shortcuts = lib_tkinter.GetButtonBar(self.root, column=0, row=1, style=style, sticky="EW", minHeight=80, commands=shortcutCommands,
                                                  labels=shortcutLabels, orientation=Orientation.HORIZONTAL)

        self.calibrationState = CalibrationState.START

    # Update
    def Update(self):
        if(self.calibrationState == CalibrationState.START):
            # Start Menu
            self.message['text'] = "Press button 1 to start calibration"
        elif(self.calibrationState == CalibrationState.REQUEST_BOTH_MIN):
            # No Pedals Menu
            self.message['text'] = "Release both pedals, then press button 1"
        elif(self.calibrationState == CalibrationState.REQUEST_APPS_MAX):
            # APPS Pedal Menu
            self.message['text'] = "Press the throttle fully, then press button 1"
        elif(self.calibrationState == CalibrationState.REQUEST_BRAKE_MAX):
            # APPS Pedal Menu
            self.message['text'] = "Press the brake fully, then press button 1"
        elif(self.calibrationState == CalibrationState.FINISHED):
            # Finished Menu
            self.message['text'] = "Calibration Finshed"
        elif(self.calibrationState == CalibrationState.FAILED):
            # Failed Menu
            self.message['text'] = "Calibration Failed"

    # Input Interrupt
    def InputInterrupt(self, input):
        # Reset Button
        if(input == database.InputTypes.BUTTON_WHEEL_LEFT):
            self.calibrationState = CalibrationState.START

        # Continue Button
        if(input == database.InputTypes.BUTTON_WHEEL_RIGHT):
            if(self.calibrationState == CalibrationState.START):
                self.calibrationState = CalibrationState.REQUEST_BOTH_MIN

            elif(self.calibrationState == CalibrationState.REQUEST_BOTH_MIN):
                self.apps1CurrentMin  = self.database["APPS_1"]
                self.apps2CurrentMin  = self.database["APPS_2"]
                self.brake1CurrentMin = self.database["Brake_1"]
                self.brake2CurrentMin = self.database["Brake_2"]
                self.calibrationState = CalibrationState.REQUEST_APPS_MAX

            elif(self.calibrationState == CalibrationState.REQUEST_APPS_MAX):
                self.apps1CurrentMax  = self.database["APPS_1"]
                self.apps2CurrentMax  = self.database["APPS_2"]
                self.calibrationState = CalibrationState.REQUEST_BRAKE_MAX

            elif(self.calibrationState == CalibrationState.REQUEST_BRAKE_MAX):
                self.brake1CurrentMax = self.database["Brake_1"]
                self.brake2CurrentMax = self.database["Brake_2"]
                self.ValidateCalibration()
                self.ApplyCalibration()

    # Validate Calibration
    # - Ensures that Calibrated Variables are Valid
    def ValidateCalibration(self):
        self.calibrationState = CalibrationState.FAILED
        if(self.apps1CurrentMin == None):    return
        if(self.apps1CurrentMax == None):    return
        if(self.apps2CurrentMin == None):    return
        if(self.apps2CurrentMax == None):    return
        if(self.brake1CurrentMin == None):   return
        if(self.brake1CurrentMax == None):   return
        if(self.brake2CurrentMin == None):   return
        if(self.brake2CurrentMax == None):   return
        if(self.apps1CurrentMin  >= self.apps1CurrentMax):  return
        if(self.apps2CurrentMin  >= self.apps2CurrentMax):  return
        if(self.brake1CurrentMin >= self.brake1CurrentMax): return
        if(self.brake2CurrentMin >= self.brake2CurrentMax): return
        self.calibrationState = CalibrationState.FINISHED

    # Apply Calibration
    # - Sends new Variables to CAN Bus
    def ApplyCalibration(self):
        if(self.calibrationState != CalibrationState.FINISHED): return
        self.database["APPS_1_Real_Min"]  = self.apps1CurrentMin
        self.database["APPS_1_Real_Max"]  = self.apps1CurrentMax
        self.database["APPS_2_Real_Min"]  = self.apps2CurrentMin
        self.database["APPS_2_Real_Max"]  = self.apps2CurrentMax
        self.database["Brake_1_Real_Min"] = self.brake1CurrentMin
        self.database["Brake_1_Real_Max"] = self.brake1CurrentMax
        self.database["Brake_2_Real_Min"] = self.brake2CurrentMin
        self.database["Brake_2_Real_Max"] = self.brake2CurrentMax
        can_interface.SendCalibrateAppsRange(self.canTransmitter, self.apps1CurrentMin, self.apps1CurrentMax, self.apps2CurrentMin, self.apps2CurrentMax)
        can_interface.SendCalibrateBrakeRange(self.canTransmitter, self.brake1CurrentMin, self.brake1CurrentMax, self.brake2CurrentMin, self.brake2CurrentMax)

    def Close(self):
        self.calibrationState = CalibrationState.START
        super().Close()