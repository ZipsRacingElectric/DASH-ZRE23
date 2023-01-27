# Libraries
import tkinter

# Includes
import lib_tkinter
import appCan
import gui

class Window(gui.Window):
    def Open(self):
        super().Open()
        self.root.title("Dashboard 2023 - Debug Module")
        self.root.resizable(0, 0)
        # Root Partitioning
        column0Width = 280
        column1Width = 600 - column0Width
        self.root.columnconfigure(0, minsize=column0Width)
        self.root.columnconfigure(1, minsize=column1Width)
        # Panel Instantiations
        inputPedalsRoot            = lib_tkinter.GetLabelFrame(self.root, label="Input Pedals: 0x005",             style=self.style, sticky="NESW", column=0, row=0)
        dataMotorRoot              = lib_tkinter.GetLabelFrame(self.root, label="Data Motor: 0x0A7",               style=self.style, sticky="NESW", column=0, row=1)
        commandAppsCalibrationRoot = lib_tkinter.GetLabelFrame(self.root, label="Command APPS Calibration: 0x533", style=self.style, sticky="NESW", column=0, row=2)
        dataPedalsRoot             = lib_tkinter.GetLabelFrame(self.root, label="Data Pedals: 0x701",              style=self.style, sticky="NESW", column=0, row=3)
        statusEcuRoot              = lib_tkinter.GetLabelFrame(self.root, label="Status ECU: 0x703",               style=self.style, sticky="NESW", column=1, row=0, rowspan=4)
        # Initializations
        self.InitializeInputPedals           (inputPedalsRoot,            column0Width)
        self.InitializeDataMotor             (dataMotorRoot,              column0Width)
        self.InitializeCommandAppsCalibration(commandAppsCalibrationRoot, column0Width)
        self.InitializeDataPedals            (dataPedalsRoot,             column0Width)
        self.InitializeStatusEcu             (statusEcuRoot,              column1Width)

    def InitializeInputPedals(self, inputPedalsRoot, width):
        # Partitioning
        buttonWidth = 40
        labelWidth = 180
        inputWidth = width - buttonWidth - labelWidth
        inputPedalsRoot.columnconfigure(0, minsize=labelWidth)
        inputPedalsRoot.columnconfigure(1, minsize=inputWidth)
        inputPedalsRoot.columnconfigure(2, minsize=buttonWidth)
        # Send Button
        lib_tkinter.GetButton(inputPedalsRoot, text="Send", command=self.SendInputPedals, column=2, row=0, sticky="E", style=self.style)
        # Labels
        lib_tkinter.GetLabel(inputPedalsRoot, text="APPS-1 Value",  column=0, row=0, sticky="W", style=self.style)
        lib_tkinter.GetLabel(inputPedalsRoot, text="APPS-2 Value",  column=0, row=1, sticky="W", style=self.style)
        lib_tkinter.GetLabel(inputPedalsRoot, text="Brake-1 Value", column=0, row=2, sticky="W", style=self.style)
        lib_tkinter.GetLabel(inputPedalsRoot, text="Brake-2 Value", column=0, row=3, sticky="W", style=self.style)
        # Inputs
        self.apps1Input  = lib_tkinter.GetEntry(inputPedalsRoot, minWidth=8, value=0, column=1, row=0, sticky="E", style=self.style)
        self.apps2Input  = lib_tkinter.GetEntry(inputPedalsRoot, minWidth=8, value=0, column=1, row=1, sticky="E", style=self.style)
        self.brake1Input = lib_tkinter.GetEntry(inputPedalsRoot, minWidth=8, value=0, column=1, row=2, sticky="E", style=self.style)
        self.brake2Input = lib_tkinter.GetEntry(inputPedalsRoot, minWidth=8, value=0, column=1, row=3, sticky="E", style=self.style)
    
    def InitializeDataMotor(self, dataMotorRoot, width):
        # Partitioning
        buttonWidth = 40
        labelWidth = 180
        inputWidth = width - buttonWidth - labelWidth
        dataMotorRoot.columnconfigure(0, minsize=labelWidth)
        dataMotorRoot.columnconfigure(1, minsize=inputWidth)
        dataMotorRoot.columnconfigure(2, minsize=buttonWidth)
        # Send Button
        lib_tkinter.GetButton(dataMotorRoot, text="Send", command=self.SendDataMotor, column=2, row=0, sticky="E", style=self.style)
        # Labels
        lib_tkinter.GetLabel(dataMotorRoot, text="Motor Angle",          column=0, row=0, sticky="W", style=self.style)
        lib_tkinter.GetLabel(dataMotorRoot, text="Motor RPM",            column=0, row=1, sticky="W", style=self.style)
        lib_tkinter.GetLabel(dataMotorRoot, text="Motor Frequency",      column=0, row=2, sticky="W", style=self.style)
        lib_tkinter.GetLabel(dataMotorRoot, text="Motor Delta Resolver", column=0, row=3, sticky="W", style=self.style)
        # Inputs
        self.motorAngleInput         = lib_tkinter.GetEntry(dataMotorRoot, minWidth=8, column=1, row=0, value=0, sticky="E", style=self.style)
        self.motorRpmInput           = lib_tkinter.GetEntry(dataMotorRoot, minWidth=8, column=1, row=1, value=0, sticky="E", style=self.style)
        self.motorFrequencyInput     = lib_tkinter.GetEntry(dataMotorRoot, minWidth=8, column=1, row=2, value=0, sticky="E", style=self.style)
        self.motorDeltaResolverInput = lib_tkinter.GetEntry(dataMotorRoot, minWidth=8, column=1, row=3, value=0, sticky="E", style=self.style)

    def InitializeCommandAppsCalibration(self, commandAppsCalibrationRoot, width):
        # Partitioning
        buttonWidth = 40
        labelWidth = 180
        inputWidth = width - buttonWidth - labelWidth
        commandAppsCalibrationRoot.columnconfigure(0, minsize=labelWidth)
        commandAppsCalibrationRoot.columnconfigure(1, minsize=inputWidth)
        commandAppsCalibrationRoot.columnconfigure(2, minsize=buttonWidth)
        # Send Button
        lib_tkinter.GetButton(commandAppsCalibrationRoot, text="Send", command=self.SendCommandAppsCalibration, column=2, row=0, sticky="E", style=self.style)
        # Labels
        lib_tkinter.GetLabel(commandAppsCalibrationRoot, text="APPS-1 Min", column=0, row=0, sticky="W", style=self.style)
        lib_tkinter.GetLabel(commandAppsCalibrationRoot, text="APPS-1 Max", column=0, row=1, sticky="W", style=self.style)
        lib_tkinter.GetLabel(commandAppsCalibrationRoot, text="APPS-2 Min", column=0, row=2, sticky="W", style=self.style)
        lib_tkinter.GetLabel(commandAppsCalibrationRoot, text="APPS-2 Max", column=0, row=3, sticky="W", style=self.style)
        # Inputs
        self.apps1MinInput = lib_tkinter.GetEntry(commandAppsCalibrationRoot, minWidth=8, column=1, row=0, value=0, sticky="E", style=self.style)
        self.apps1MaxInput = lib_tkinter.GetEntry(commandAppsCalibrationRoot, minWidth=8, column=1, row=1, value=0, sticky="E", style=self.style)
        self.apps2MinInput = lib_tkinter.GetEntry(commandAppsCalibrationRoot, minWidth=8, column=1, row=2, value=0, sticky="E", style=self.style)
        self.apps2MaxInput = lib_tkinter.GetEntry(commandAppsCalibrationRoot, minWidth=8, column=1, row=3, value=0, sticky="E", style=self.style)

    def InitializeDataPedals(self, dataPedalsRoot, width):
        # Partitioning
        buttonWidth = 40
        labelWidth = 180
        inputWidth = width - buttonWidth - labelWidth
        dataPedalsRoot.columnconfigure(0, minsize=labelWidth)
        dataPedalsRoot.columnconfigure(1, minsize=inputWidth)
        dataPedalsRoot.columnconfigure(2, minsize=buttonWidth)
        # Send Button
        lib_tkinter.GetButton(dataPedalsRoot, text="Send", command=self.SendDataPedals, column=2, row=0, sticky="E", style=self.style)
        # Labels
        lib_tkinter.GetLabel(dataPedalsRoot, text="APPS-1 Percent",  column=0, row=0, sticky="W", style=self.style)
        lib_tkinter.GetLabel(dataPedalsRoot, text="APPS-2 Percent",  column=0, row=1, sticky="W", style=self.style)
        lib_tkinter.GetLabel(dataPedalsRoot, text="Brake-1 Percent", column=0, row=2, sticky="W", style=self.style)
        lib_tkinter.GetLabel(dataPedalsRoot, text="Brake-2 Percent", column=0, row=3, sticky="W", style=self.style)
        # Inputs
        self.apps1PercentInput  = lib_tkinter.GetEntry(dataPedalsRoot, minWidth=8, column=1, row=0, value=0, sticky="E", style=self.style)
        self.apps2PercentInput  = lib_tkinter.GetEntry(dataPedalsRoot, minWidth=8, column=1, row=1, value=0, sticky="E", style=self.style)
        self.brake1PercentInput = lib_tkinter.GetEntry(dataPedalsRoot, minWidth=8, column=1, row=2, value=0, sticky="E", style=self.style)
        self.brake2PercentInput = lib_tkinter.GetEntry(dataPedalsRoot, minWidth=8, column=1, row=3, value=0, sticky="E", style=self.style)
  
    def InitializeStatusEcu(self, statusEcuRoot, width):
        # Partitioning
        buttonWidth = 40
        labelWidth = 165
        inputWidth = width - buttonWidth - labelWidth
        statusEcuRoot.columnconfigure(0, minsize=labelWidth)
        statusEcuRoot.columnconfigure(1, minsize=inputWidth)
        statusEcuRoot.columnconfigure(2, minsize=buttonWidth)
        # Send Button
        lib_tkinter.GetButton(statusEcuRoot, text="Send", command=self.SendStatusEcu, column=2, row=0, sticky="E", style=self.style)
        # Labels
        lib_tkinter.GetLabel(statusEcuRoot, text="Drive State",           column=0, row=0,  sticky="W", style=self.style)
        lib_tkinter.GetLabel(statusEcuRoot, text="Is Accelerating",       column=0, row=1,  sticky="W", style=self.style)
        lib_tkinter.GetLabel(statusEcuRoot, text="Is Braking",            column=0, row=2,  sticky="W", style=self.style)
        lib_tkinter.GetLabel(statusEcuRoot, text="DRS Enabled",           column=0, row=3,  sticky="W", style=self.style)
        lib_tkinter.GetLabel(statusEcuRoot, text="Regen Enabled",         column=0, row=4,  sticky="W", style=self.style)
        lib_tkinter.GetLabel(statusEcuRoot, text="25/5 Implausible",      column=0, row=5,  sticky="W", style=self.style)
        lib_tkinter.GetLabel(statusEcuRoot, text="Inverter Fault",        column=0, row=6,  sticky="W", style=self.style)
        lib_tkinter.GetLabel(statusEcuRoot, text="ACAN Implausible",      column=0, row=7,  sticky="W", style=self.style)
        lib_tkinter.GetLabel(statusEcuRoot, text="100ms Implausible",     column=0, row=8,  sticky="W", style=self.style)
        lib_tkinter.GetLabel(statusEcuRoot, text="Torque Percentage Max", column=0, row=9,  sticky="W", style=self.style)
        lib_tkinter.GetLabel(statusEcuRoot, text="Regen Percentage Max",  column=0, row=10, sticky="W", style=self.style)
        lib_tkinter.GetLabel(statusEcuRoot, text="LV Battery Voltage",    column=0, row=11, sticky="W", style=self.style)
        lib_tkinter.GetLabel(statusEcuRoot, text="IMD Resistance",        column=0, row=12, sticky="W", style=self.style)
        # Inputs
        self.driveStateInput   = tkinter.IntVar(value=0)
        self.acceleratingInput = tkinter.BooleanVar(value=False)
        self.brakingInput      = tkinter.BooleanVar(value=False)
        self.drsInput          = tkinter.BooleanVar(value=False)
        self.regenInput        = tkinter.BooleanVar(value=False)
        self.is25_5Input       = tkinter.BooleanVar(value=False)
        self.inverterInput     = tkinter.BooleanVar(value=False)
        self.acanInput         = tkinter.BooleanVar(value=False)
        self.is100msInput      = tkinter.BooleanVar(value=False)
        # Selection Inputs
        driveStateFrame = lib_tkinter.GetFrame(statusEcuRoot, column=1, row=0, style=self.style)
        lib_tkinter.GetRadiobutton(driveStateFrame, variable=self.driveStateInput, text="Initializing", value=0, column=0,row=0, sticky="W", style=self.style)
        lib_tkinter.GetRadiobutton(driveStateFrame, variable=self.driveStateInput, text="LV Drive OFF", value=1, column=0,row=1, sticky="W", style=self.style)
        lib_tkinter.GetRadiobutton(driveStateFrame, variable=self.driveStateInput, text="HV Drive OFF", value=2, column=0,row=2, sticky="W", style=self.style)
        lib_tkinter.GetRadiobutton(driveStateFrame, variable=self.driveStateInput, text="HV Drive ON",  value=3, column=0,row=3, sticky="W", style=self.style)
        # Boolean Inputs
        lib_tkinter.GetCheckbutton(statusEcuRoot, variable=self.acceleratingInput, column=1, row=1, sticky="W", style=self.style)
        lib_tkinter.GetCheckbutton(statusEcuRoot, variable=self.brakingInput,      column=1, row=2, sticky="W", style=self.style)
        lib_tkinter.GetCheckbutton(statusEcuRoot, variable=self.drsInput,          column=1, row=3, sticky="W", style=self.style)
        lib_tkinter.GetCheckbutton(statusEcuRoot, variable=self.regenInput,        column=1, row=4, sticky="W", style=self.style)
        lib_tkinter.GetCheckbutton(statusEcuRoot, variable=self.is25_5Input,       column=1, row=5, sticky="W", style=self.style)
        lib_tkinter.GetCheckbutton(statusEcuRoot, variable=self.inverterInput,     column=1, row=6, sticky="W", style=self.style)
        lib_tkinter.GetCheckbutton(statusEcuRoot, variable=self.acanInput,         column=1, row=7, sticky="W", style=self.style)
        lib_tkinter.GetCheckbutton(statusEcuRoot, variable=self.is100msInput,      column=1, row=8, sticky="W", style=self.style)
        # Numeric Inputs
        self.torquePercentInput = lib_tkinter.GetEntry(statusEcuRoot, minWidth=16, column=1, row=9,  value=0, sticky="E", style=self.style)
        self.regenPercentInput  = lib_tkinter.GetEntry(statusEcuRoot, minWidth=16, column=1, row=10, value=0, sticky="E", style=self.style)
        self.voltageLvInput     = lib_tkinter.GetEntry(statusEcuRoot, minWidth=16, column=1, row=11, value=0, sticky="E", style=self.style)
        self.resistanceImdInput = lib_tkinter.GetEntry(statusEcuRoot, minWidth=16, column=1, row=12, value=0, sticky="E", style=self.style)

    def SendInputPedals(self):
        apps1  = int(self.apps1Input.get())
        apps2  = int(self.apps2Input.get())
        brake1 = int(self.brake1Input.get())
        brake2 = int(self.brake2Input.get())
        appCan.SendInputPedals(apps1, apps2, brake1, brake2)

    def SendDataMotor(self):
        motorAngle         = int(self.motorAngleInput.get())
        motorRpm           = int(self.motorRpmInput.get())
        motorFrequency     = int(self.motorFrequencyInput.get())
        motorDeltaResolver = int(self.motorDeltaResolverInput.get())
        appCan.SendDataMotor(motorAngle, motorRpm, motorFrequency, motorDeltaResolver)

    def SendCommandAppsCalibration(self):
        apps1MinValue = int(self.apps1MinInput.get())
        apps1MaxValue = int(self.apps1MaxInput.get())
        apps2MinValue = int(self.apps2MinInput.get())
        apps2MaxValue = int(self.apps2MaxInput.get())
        appCan.SendCommandAppsCalibration(apps1MinValue, apps1MaxValue, apps2MinValue, apps2MaxValue)

    def SendDataPedals(self):
        apps1Percent  = int(self.apps1PercentInput.get())
        apps2Percent  = int(self.apps2PercentInput.get())
        brake1Percent = int(self.brake1PercentInput.get())
        brake2Percent = int(self.brake2PercentInput.get())
        appCan.SendDataPedals(apps1Percent, apps2Percent, brake1Percent, brake2Percent)

    def SendStatusEcu(self):
        driveStateValue    = int(self.driveStateInput.get())
        acceleratingValue  = self.acceleratingInput.get()
        brakingValue       = self.brakingInput.get()
        drsValue           = self.drsInput.get()
        regenValue         = self.regenInput.get()
        is25_5Value        = self.is25_5Input.get()
        inverterValue      = self.inverterInput.get()
        acanValue          = self.acanInput.get()
        is100msValue       = self.is100msInput.get()
        torquePercentValue = int(self.torquePercentInput.get())
        regenPercentValue  = int(self.regenPercentInput.get())
        voltageLvValue     = float(self.voltageLvInput.get())
        resistanceImdValue = float(self.resistanceImdInput.get())
        appCan.SendStatusEcu(driveStateValue, acceleratingValue, brakingValue, drsValue, regenValue, is25_5Value, inverterValue, acanValue, is100msValue, torquePercentValue, regenPercentValue, voltageLvValue, resistanceImdValue)