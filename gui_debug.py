# Debug GUI View ----------------------------------------------------------------------------------------------------------
# Author: Cole Barach
# Date Created: 22.11.07
# Date Updated: 23.01.30
#   This module contains all objects related to the Debug View of the GUI. The Window object may be instanced to create a
#   window capable of performing any debug behavior.

# Libraries -------------------------------------------------------------------------------------------------------------------
import tkinter
import lib_tkinter
from lib_tkinter import Orientation

# Includes --------------------------------------------------------------------------------------------------------------------
import gui
import can_interface

import log
from log import print

# Objects ---------------------------------------------------------------------------------------------------------------------
class View(gui.View):
    # Initialization
    def __init__(self, gui, id, style, database, can):
        super().__init__(gui, id, style, database)
        self.can = can
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(   0, weight=1)
        self.scrollFrame = lib_tkinter.GetScrollFrame(self.root, self.style, Orientation.VERTICAL, sticky="NESW")
        self.frame = self.scrollFrame.Get()

        self.database = database

        # Root Partitioning
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

        labelWidth = 180 # Label Column
        statWidth  = 180 # Stat Column Width

        fontBoldOverride = [("font", "fontBold")]

        rowIndex = 0

        self.commands = []
        self.widgets = []
        self.inputs = []

        for message in database.db.messages:
            messageFrame = lib_tkinter.GetFrame(self.frame, style=style, border=True, column=0, row=rowIndex, sticky="NESW")

            self.commands.append(lambda id = message.frame_id: self.SendMessage(id))

            label  = lib_tkinter.GetLabel(messageFrame,  style=style, column=0, row=0, columnspan=2, text=f"{message.name} ({hex(message.frame_id)})", sticky="NW", styleOverrides=fontBoldOverride)
            button = lib_tkinter.GetButton(messageFrame, style=style, column=2, row=0, text="Send", sticky="NE", command=self.commands[len(self.commands)-1])
            
            self.widgets.append((label, button))
            
            rowIndex += 1

            messageFrame.columnconfigure(0, minsize=labelWidth)
            messageFrame.columnconfigure(1, weight=1)
            messageFrame.columnconfigure(2, minsize=statWidth)
            
            subIndex = 1
            
            for signal in message.signals:
                lib_tkinter.GetLabel(messageFrame, style=style, column=0, row=subIndex, text=f"  {signal.name}", sticky="NW")

                if(signal.unit == "Boolean"):
                    variable = tkinter.BooleanVar(self.frame)
                    entry = lib_tkinter.GetCheckbutton(messageFrame, variable=variable, style=style, column=2, row=subIndex, sticky="NE")

                    self.inputs.append((message.frame_id, signal.name, variable, entry, "bool"))
                else:
                    variable = tkinter.StringVar(self.frame)
                    entry = lib_tkinter.GetEntry(messageFrame, variable=variable, minWidth=4, style=style, column=2, row=subIndex, sticky="NEW")

                    self.inputs.append((message.frame_id, signal.name, variable, entry, "int"))

                subIndex += 1

    def Open(self):
        super().Open()

    def SendMessage(self, id):
        messageDatabase = dict()

        for input in self.inputs:
            if(input[0] == id):
                if(input[4] == "bool"):
                    self.database[input[1]] = bool(input[2].get())
                    messageDatabase[input[1]] = self.database[input[1]]
                else:
                    if(input[2].get() != ""):
                        self.database[input[1]] = int(input[2].get())
                    else:
                        self.database[input[1]] = 0
                    messageDatabase[input[1]] = self.database[input[1]]

        dataOut = self.database.db.encode_message(id, messageDatabase)

        data = [0,0,0,0,0,0,0,0]
        i = 0
        for byte in dataOut:
            data[i] = byte
            i += 1
        
        can_interface.SendMessage(self.can, id, data)
                    

# DEPRICATED ------------------------------------------------------------------------------------------------------------------

        # # Panel Instantiations
        # inputPedalsRoot            = lib_tkinter.GetLabelFrame(self.frame, label="Input Pedals: 0x005",                style=self.style, sticky="NESW", column=0, row=0)
        # dataMotorRoot              = lib_tkinter.GetLabelFrame(self.frame, label="Data Motor: 0x0A7",                  style=self.style, sticky="NESW", column=0, row=1)
        # commandAppsCalibrationRoot = lib_tkinter.GetLabelFrame(self.frame, label="Command APPS Calibration: 0x533",    style=self.style, sticky="NESW", column=0, row=2)
        # dataPedalsRoot             = lib_tkinter.GetLabelFrame(self.frame, label="Data Pedals: 0x701",                 style=self.style, sticky="NESW", column=0, row=3)
        # commandTorqueLimitRoot     = lib_tkinter.GetLabelFrame(self.frame, label="Command Drive Configuration: 0x010", style=self.style, sticky="NESW", column=0, row=4)
        # statusEcuRoot              = lib_tkinter.GetLabelFrame(self.frame, label="Status ECU: 0x703",                  style=self.style, sticky="NESW", column=1, row=0, rowspan=4)
        # commandDriveStart          = lib_tkinter.GetLabelFrame(self.frame, label="Command Drive Start: 0x004",         style=self.style, sticky="NESW", column=1, row=4)
        # # Initializations
        # self.InitializeInputPedals              (inputPedalsRoot)
        # self.InitializeDataMotor                (dataMotorRoot)
        # self.InitializeCommandAppsCalibration   (commandAppsCalibrationRoot)
        # self.InitializeDataPedals               (dataPedalsRoot)
        # self.InitializeCommandDriveConfiguration(commandTorqueLimitRoot)
        # self.InitializeStatusEcu                (statusEcuRoot)
        # self.InitializeCommandDriveStart        (commandDriveStart)

    # # Breakout Initializers ---------------------------------------------------------------------------------------------------
    # def InitializeInputPedals(self, inputPedalsRoot):
    #     # Partitioning
    #     buttonWidth = 40
    #     labelWidth = 180
    #     inputPedalsRoot.columnconfigure(0, minsize=labelWidth)
    #     inputPedalsRoot.columnconfigure(1, weight=1)
    #     inputPedalsRoot.columnconfigure(2, minsize=buttonWidth)
    #     # Send Button
    #     lib_tkinter.GetButton(inputPedalsRoot, text="Send", command=self.SendInputPedals, column=2, row=0, sticky="E", style=self.style)
    #     # Labels
    #     lib_tkinter.GetLabel(inputPedalsRoot, text="APPS-1 Value",  column=0, row=0, sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(inputPedalsRoot, text="APPS-2 Value",  column=0, row=1, sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(inputPedalsRoot, text="Brake-1 Value", column=0, row=2, sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(inputPedalsRoot, text="Brake-2 Value", column=0, row=3, sticky="W", style=self.style)
    #     # Inputs
    #     self.apps1Input  = lib_tkinter.GetEntry(inputPedalsRoot, minWidth=8, value=0, column=1, row=0, sticky="E", style=self.style)
    #     self.apps2Input  = lib_tkinter.GetEntry(inputPedalsRoot, minWidth=8, value=0, column=1, row=1, sticky="E", style=self.style)
    #     self.brake1Input = lib_tkinter.GetEntry(inputPedalsRoot, minWidth=8, value=0, column=1, row=2, sticky="E", style=self.style)
    #     self.brake2Input = lib_tkinter.GetEntry(inputPedalsRoot, minWidth=8, value=0, column=1, row=3, sticky="E", style=self.style)
    
    # def InitializeDataMotor(self, dataMotorRoot):
    #     # Partitioning
    #     buttonWidth = 40
    #     labelWidth = 180
    #     dataMotorRoot.columnconfigure(0, minsize=labelWidth)
    #     dataMotorRoot.columnconfigure(1, weight=1)
    #     dataMotorRoot.columnconfigure(2, minsize=buttonWidth)
    #     # Send Button
    #     lib_tkinter.GetButton(dataMotorRoot, text="Send", command=self.SendDataMotor, column=2, row=0, sticky="E", style=self.style)
    #     # Labels
    #     lib_tkinter.GetLabel(dataMotorRoot, text="Motor Angle",          column=0, row=0, sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(dataMotorRoot, text="Motor RPM",            column=0, row=1, sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(dataMotorRoot, text="Motor Frequency",      column=0, row=2, sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(dataMotorRoot, text="Motor Delta Resolver", column=0, row=3, sticky="W", style=self.style)
    #     # Inputs
    #     self.motorAngleInput         = lib_tkinter.GetEntry(dataMotorRoot, minWidth=8, column=1, row=0, value=0, sticky="E", style=self.style)
    #     self.motorRpmInput           = lib_tkinter.GetEntry(dataMotorRoot, minWidth=8, column=1, row=1, value=0, sticky="E", style=self.style)
    #     self.motorFrequencyInput     = lib_tkinter.GetEntry(dataMotorRoot, minWidth=8, column=1, row=2, value=0, sticky="E", style=self.style)
    #     self.motorDeltaResolverInput = lib_tkinter.GetEntry(dataMotorRoot, minWidth=8, column=1, row=3, value=0, sticky="E", style=self.style)

    # def InitializeCommandAppsCalibration(self, commandAppsCalibrationRoot):
    #     # Partitioning
    #     buttonWidth = 40
    #     labelWidth = 180
    #     commandAppsCalibrationRoot.columnconfigure(0, minsize=labelWidth)
    #     commandAppsCalibrationRoot.columnconfigure(1, weight=1)
    #     commandAppsCalibrationRoot.columnconfigure(2, minsize=buttonWidth)
    #     # Send Button
    #     lib_tkinter.GetButton(commandAppsCalibrationRoot, text="Send", command=self.SendCommandAppsCalibration, column=2, row=0, sticky="E", style=self.style)
    #     # Labels
    #     lib_tkinter.GetLabel(commandAppsCalibrationRoot, text="APPS-1 Min", column=0, row=0, sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(commandAppsCalibrationRoot, text="APPS-1 Max", column=0, row=1, sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(commandAppsCalibrationRoot, text="APPS-2 Min", column=0, row=2, sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(commandAppsCalibrationRoot, text="APPS-2 Max", column=0, row=3, sticky="W", style=self.style)
    #     # Inputs
    #     self.apps1MinInput = lib_tkinter.GetEntry(commandAppsCalibrationRoot, minWidth=8, column=1, row=0, value=0, sticky="E", style=self.style)
    #     self.apps1MaxInput = lib_tkinter.GetEntry(commandAppsCalibrationRoot, minWidth=8, column=1, row=1, value=0, sticky="E", style=self.style)
    #     self.apps2MinInput = lib_tkinter.GetEntry(commandAppsCalibrationRoot, minWidth=8, column=1, row=2, value=0, sticky="E", style=self.style)
    #     self.apps2MaxInput = lib_tkinter.GetEntry(commandAppsCalibrationRoot, minWidth=8, column=1, row=3, value=0, sticky="E", style=self.style)

    # def InitializeDataPedals(self, dataPedalsRoot):
    #     # Partitioning
    #     buttonWidth = 40
    #     labelWidth = 180
    #     dataPedalsRoot.columnconfigure(0, minsize=labelWidth)
    #     dataPedalsRoot.columnconfigure(1, weight=1)
    #     dataPedalsRoot.columnconfigure(2, minsize=buttonWidth)
    #     # Send Button
    #     lib_tkinter.GetButton(dataPedalsRoot, text="Send", command=self.SendDataPedals, column=2, row=0, sticky="E", style=self.style)
    #     # Labels
    #     lib_tkinter.GetLabel(dataPedalsRoot, text="APPS-1 Percent",  column=0, row=0, sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(dataPedalsRoot, text="APPS-2 Percent",  column=0, row=1, sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(dataPedalsRoot, text="Brake-1 Percent", column=0, row=2, sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(dataPedalsRoot, text="Brake-2 Percent", column=0, row=3, sticky="W", style=self.style)
    #     # Inputs
    #     self.apps1PercentInput  = lib_tkinter.GetEntry(dataPedalsRoot, minWidth=8, column=1, row=0, value=0, sticky="E", style=self.style)
    #     self.apps2PercentInput  = lib_tkinter.GetEntry(dataPedalsRoot, minWidth=8, column=1, row=1, value=0, sticky="E", style=self.style)
    #     self.brake1PercentInput = lib_tkinter.GetEntry(dataPedalsRoot, minWidth=8, column=1, row=2, value=0, sticky="E", style=self.style)
    #     self.brake2PercentInput = lib_tkinter.GetEntry(dataPedalsRoot, minWidth=8, column=1, row=3, value=0, sticky="E", style=self.style)
  
    # def InitializeCommandDriveConfiguration(self, commandTorqueLimitRoot):
    #     # Partitioning
    #     buttonWidth = 40
    #     labelWidth = 180
    #     commandTorqueLimitRoot.columnconfigure(0, minsize=labelWidth)
    #     commandTorqueLimitRoot.columnconfigure(1, weight=1)
    #     commandTorqueLimitRoot.columnconfigure(2, minsize=buttonWidth)
    #     # Send Button
    #     lib_tkinter.GetButton(commandTorqueLimitRoot, text="Send", command=self.SendCommandDriveConfiguration, column=2, row=0, sticky="E", style=self.style)
    #     # Labels
    #     lib_tkinter.GetLabel(commandTorqueLimitRoot, text="Torque Limit",  column=0, row=0, sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(commandTorqueLimitRoot, text="Regen Limit",   column=0, row=1, sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(commandTorqueLimitRoot, text="Regen Enabled", column=0, row=2, sticky="W", style=self.style)
    #     # Inputs
    #     self.regenEnableInput = tkinter.BooleanVar(value=False)

    #     self.torqueInput      = lib_tkinter.GetEntry      (commandTorqueLimitRoot, minWidth=8, value=0, column=1, row=0, sticky="E", style=self.style)
    #     self.regenTorqueInput = lib_tkinter.GetEntry      (commandTorqueLimitRoot, minWidth=8, value=0, column=1, row=1, sticky="E", style=self.style)
    #     self.regenEnableCheck = lib_tkinter.GetCheckbutton(commandTorqueLimitRoot, variable=self.regenEnableInput, column=1, row=2, sticky="E", style=self.style)

    # def InitializeStatusEcu(self, statusEcuRoot):
    #     # Partitioning
    #     buttonWidth = 40
    #     labelWidth = 165
    #     statusEcuRoot.columnconfigure(0, minsize=labelWidth)
    #     statusEcuRoot.columnconfigure(1, weight=1)
    #     statusEcuRoot.columnconfigure(2, minsize=buttonWidth)
    #     # Send Button
    #     lib_tkinter.GetButton(statusEcuRoot, text="Send", command=self.SendStatusEcu, column=2, row=0, sticky="NE", style=self.style)
    #     # Labels
    #     lib_tkinter.GetLabel(statusEcuRoot, text="Drive State",           column=0, row=0,  sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(statusEcuRoot, text="Is Accelerating",       column=0, row=1,  sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(statusEcuRoot, text="Is Braking",            column=0, row=2,  sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(statusEcuRoot, text="DRS Enabled",           column=0, row=3,  sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(statusEcuRoot, text="Regen Enabled",         column=0, row=4,  sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(statusEcuRoot, text="25/5 Implausible",      column=0, row=5,  sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(statusEcuRoot, text="Inverter Fault",        column=0, row=6,  sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(statusEcuRoot, text="ACAN Implausible",      column=0, row=7,  sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(statusEcuRoot, text="100ms Implausible",     column=0, row=8,  sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(statusEcuRoot, text="Torque Percentage Max", column=0, row=9,  sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(statusEcuRoot, text="Regen Percentage Max",  column=0, row=10, sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(statusEcuRoot, text="LV Battery Voltage",    column=0, row=11, sticky="W", style=self.style)
    #     lib_tkinter.GetLabel(statusEcuRoot, text="IMD Resistance",        column=0, row=12, sticky="W", style=self.style)
    #     # Inputs
    #     self.driveStateInput   = tkinter.IntVar(value=0)
    #     self.acceleratingInput = tkinter.BooleanVar(value=False)
    #     self.brakingInput      = tkinter.BooleanVar(value=False)
    #     self.drsInput          = tkinter.BooleanVar(value=False)
    #     self.regenInput        = tkinter.BooleanVar(value=False)
    #     self.is25_5Input       = tkinter.BooleanVar(value=False)
    #     self.inverterInput     = tkinter.BooleanVar(value=False)
    #     self.acanInput         = tkinter.BooleanVar(value=False)
    #     self.is100msInput      = tkinter.BooleanVar(value=False)
    #     # Selection Inputs
    #     driveStateFrame = lib_tkinter.GetFrame(statusEcuRoot, column=1, row=0, style=self.style)
    #     lib_tkinter.GetRadiobutton(driveStateFrame, variable=self.driveStateInput, text="Initializing", value=0, column=0,row=0, sticky="W", style=self.style)
    #     lib_tkinter.GetRadiobutton(driveStateFrame, variable=self.driveStateInput, text="LV Drive OFF", value=1, column=0,row=1, sticky="W", style=self.style)
    #     lib_tkinter.GetRadiobutton(driveStateFrame, variable=self.driveStateInput, text="HV Drive OFF", value=2, column=0,row=2, sticky="W", style=self.style)
    #     lib_tkinter.GetRadiobutton(driveStateFrame, variable=self.driveStateInput, text="HV Drive ON",  value=3, column=0,row=3, sticky="W", style=self.style)
    #     # Boolean Inputs
    #     lib_tkinter.GetCheckbutton(statusEcuRoot, variable=self.acceleratingInput, column=1, row=1, sticky="E", style=self.style)
    #     lib_tkinter.GetCheckbutton(statusEcuRoot, variable=self.brakingInput,      column=1, row=2, sticky="E", style=self.style)
    #     lib_tkinter.GetCheckbutton(statusEcuRoot, variable=self.drsInput,          column=1, row=3, sticky="E", style=self.style)
    #     lib_tkinter.GetCheckbutton(statusEcuRoot, variable=self.regenInput,        column=1, row=4, sticky="E", style=self.style)
    #     lib_tkinter.GetCheckbutton(statusEcuRoot, variable=self.is25_5Input,       column=1, row=5, sticky="E", style=self.style)
    #     lib_tkinter.GetCheckbutton(statusEcuRoot, variable=self.inverterInput,     column=1, row=6, sticky="E", style=self.style)
    #     lib_tkinter.GetCheckbutton(statusEcuRoot, variable=self.acanInput,         column=1, row=7, sticky="E", style=self.style)
    #     lib_tkinter.GetCheckbutton(statusEcuRoot, variable=self.is100msInput,      column=1, row=8, sticky="E", style=self.style)
    #     # Numeric Inputs
    #     self.torquePercentInput = lib_tkinter.GetEntry(statusEcuRoot, minWidth=16, column=1, row=9,  value=0, sticky="E", style=self.style)
    #     self.regenPercentInput  = lib_tkinter.GetEntry(statusEcuRoot, minWidth=16, column=1, row=10, value=0, sticky="E", style=self.style)
    #     self.voltageLvInput     = lib_tkinter.GetEntry(statusEcuRoot, minWidth=16, column=1, row=11, value=0, sticky="E", style=self.style)
    #     self.resistanceImdInput = lib_tkinter.GetEntry(statusEcuRoot, minWidth=16, column=1, row=12, value=0, sticky="E", style=self.style)
        
    # def InitializeCommandDriveStart(self, commandDriveStartRoot):
    #     # Partitioning
    #     buttonWidth = 40
    #     labelWidth = 165
    #     commandDriveStartRoot.columnconfigure(0, minsize=labelWidth)
    #     commandDriveStartRoot.columnconfigure(1, weight=1)
    #     commandDriveStartRoot.columnconfigure(2, minsize=buttonWidth)
    #     # Send Button
    #     lib_tkinter.GetButton(commandDriveStartRoot, text="Send", command=self.SendCommandDriveConfiguration, column=2, row=0, sticky="E", style=self.style)
    #     # Labels
    #     lib_tkinter.GetLabel(commandDriveStartRoot, text="Start", column=0, row=0, sticky="W", style=self.style)
    #     # Inputs
    #     self.commandStartInput = tkinter.BooleanVar(value=True)
    #     # Boolean Inputs
    #     lib_tkinter.GetCheckbutton(commandDriveStartRoot, variable=self.commandStartInput, column=1, row=0, sticky="E", style=self.style)
        
    # # Transmitters ------------------------------------------------------------------------------------------------------------
    # def SendInputPedals(self):
    #     apps1  = int(self.apps1Input.get())
    #     apps2  = int(self.apps2Input.get())
    #     brake1 = int(self.brake1Input.get())
    #     brake2 = int(self.brake2Input.get())
    #     can_interface.SendInputPedals(self.can, apps1, apps2, brake1, brake2)

    # def SendDataMotor(self):
    #     motorAngle         = int(self.motorAngleInput.get())
    #     motorRpm           = int(self.motorRpmInput.get())
    #     motorFrequency     = int(self.motorFrequencyInput.get())
    #     motorDeltaResolver = int(self.motorDeltaResolverInput.get())
    #     can_interface.SendDataMotor(self.can, motorAngle, motorRpm, motorFrequency, motorDeltaResolver)

    # def SendCommandAppsCalibration(self):
    #     apps1MinValue = int(self.apps1MinInput.get())
    #     apps1MaxValue = int(self.apps1MaxInput.get())
    #     apps2MinValue = int(self.apps2MinInput.get())
    #     apps2MaxValue = int(self.apps2MaxInput.get())
    #     can_interface.SendCommandAppsCalibration(self.can, apps1MinValue, apps1MaxValue, apps2MinValue, apps2MaxValue)

    # def SendDataPedals(self):
    #     apps1Percent  = int(self.apps1PercentInput.get())
    #     apps2Percent  = int(self.apps2PercentInput.get())
    #     brake1Percent = int(self.brake1PercentInput.get())
    #     brake2Percent = int(self.brake2PercentInput.get())
    #     can_interface.SendDataPedals(self.can, apps1Percent, apps2Percent, brake1Percent, brake2Percent)

    # def SendCommandDriveConfiguration(self):
    #     torqueLimit  = float(self.torqueInput.get())
    #     regenLimit   = float(self.regenTorqueInput.get())
    #     regenEnabled = self.regenEnableInput.get()
    #     can_interface.SendCommandDriveConfiguration(self.can, torqueLimit, regenLimit, regenEnabled)

    # def SendStatusEcu(self):
    #     print("DEBUG - DEPRECATED CODE.")
    #     driveStateValue    = int(self.driveStateInput.get())
    #     acceleratingValue  = self.acceleratingInput.get()
    #     brakingValue       = self.brakingInput.get()
    #     drsValue           = self.drsInput.get()
    #     regenValue         = self.regenInput.get()
    #     is25_5Value        = self.is25_5Input.get()
    #     inverterValue      = self.inverterInput.get()
    #     acanValue          = self.acanInput.get()
    #     is100msValue       = self.is100msInput.get()
    #     torquePercentValue = int(self.torquePercentInput.get())
    #     regenPercentValue  = int(self.regenPercentInput.get())
    #     voltageLvValue     = float(self.voltageLvInput.get())
    #     resistanceImdValue = float(self.resistanceImdInput.get())
    #     can_interface.SendStatusEcu(self.can, driveStateValue, acceleratingValue, brakingValue, drsValue, regenValue, is25_5Value, inverterValue, acanValue, is100msValue, torquePercentValue, regenPercentValue, voltageLvValue, resistanceImdValue)

    # def SendCommandDriveConfiguration(self):
    #     start = self.commandStartInput.get()
    #     can_interface.SendCommandDriveStart(self.can, start)