import enum
from enum import Enum

import lib_tkinter
from lib_tkinter import Orientation

import gui
import config

import appCan

class CalibrationState(Enum): # State of Calibration
    START                = 0, # - Buffer menu to avoid accidental calibration
    REQUEST_APPS_MIN     = 1, # - For minimum values, tells the driver to not touch pedals
    REQUEST_APPS_MAX     = 2, # - For maximum values, tells the driver to press throttle
    FINISHED             = 3, # - For Valid Calibration Only
    FAILED               = 4  # - For Invalid Calibration

class View(gui.View):
    def __init__(self, parent, id, style, database):
        # Root --------------------------------------------------------------------------------------------------------------------------------------------------------
        super().__init__(parent, id, style, database)

        # Root Partitioning -----------------------------------------------------------------------------------
        shortcutCommands = [lambda: self.parent.CloseViews(),
                            lambda: self.InputInterrupt(0),
                            lambda: self.InputInterrupt(1),
                            0]
        shortcutLabels   = ["Back", 
                            "Next",
                            "Reset",
                            ""]
        
        self.root.columnconfigure(index=0, weight=1)
        self.root.rowconfigure(   index=0, weight=1)
        self.root.rowconfigure(   index=1, weight=0)

        # Root Widgets ----------------------------------------------------------------------------------------
        self.message   = lib_tkinter.GetLabel    (self.root, column=0, row=0, style=style, sticky="EW")
        self.shortcuts = lib_tkinter.GetButtonBar(self.root, column=0, row=1, style=style, sticky="EW", minHeight=80, commands=shortcutCommands, labels=shortcutLabels, orientation=Orientation.HORIZONTAL)

        self.calibrationState = CalibrationState.START

    # View Update Interrupt
    def Update(self):
        if(self.calibrationState == CalibrationState.START):
            # Start Menu
            self.message['text'] = "Press button 1 to start calibration"
        elif(self.calibrationState == CalibrationState.REQUEST_APPS_MIN):
            # No Pedals Menu
            self.message['text'] = "Release both pedals, then press button 1"
        elif(self.calibrationState == CalibrationState.REQUEST_APPS_MAX):
            # APPS Pedal Menu
            self.message['text'] = "Press the throttle fully, then press button 1"
        elif(self.calibrationState == CalibrationState.FINISHED):
            # Finished Menu
            self.message['text'] = "Calibration Finshed"
        elif(self.calibrationState == CalibrationState.FAILED):
            # Failed Menu
            self.message['text'] = "Calibration Failed"

    # Inputs
    def InputInterrupt(self, interruptId):
        if(interruptId == 1):
            self.calibrationState = CalibrationState.START
        if(interruptId == 0):
            if(self.calibrationState == CalibrationState.START):
                self.calibrationState = CalibrationState.REQUEST_APPS_MIN

            elif(self.calibrationState == CalibrationState.REQUEST_APPS_MIN):
                self.apps1CurrentMin    = self.database.apps1
                self.apps2RawCurrentMin = self.database.apps2Raw
                self.calibrationState = CalibrationState.REQUEST_APPS_MAX

            elif(self.calibrationState == CalibrationState.REQUEST_APPS_MAX):
                self.apps1CurrentMax    = self.database.apps1
                self.apps2RawCurrentMax = self.database.apps2Raw
                self.ValidateCalibration()
                self.ApplyCalibration()

    def ValidateCalibration(self):
        self.calibrationState = CalibrationState.FAILED
        if(self.apps1CurrentMin == None):    return
        if(self.apps1CurrentMax == None):    return
        if(self.apps2RawCurrentMin == None): return
        if(self.apps2RawCurrentMax == None): return
        if(self.apps1CurrentMin    >= self.apps1CurrentMax):    return
        if(self.apps2RawCurrentMin >= self.apps2RawCurrentMax): return
        self.calibrationState = CalibrationState.FINISHED

    def ApplyCalibration(self):
        if(self.calibrationState != CalibrationState.FINISHED): return
        self.database.apps1Min    = self.apps1CurrentMin
        self.database.apps1Max    = self.apps1CurrentMax
        self.database.apps2RawMin = self.apps2RawCurrentMin
        self.database.apps2RawMax = self.apps2RawCurrentMax
        appCan.SendCommandAppsCalibration(self.apps1CurrentMin, self.apps1CurrentMax, self.apps2RawCurrentMin, self.apps2RawCurrentMax)

    def Close(self):
        self.calibrationState = CalibrationState.START
        super().Close()