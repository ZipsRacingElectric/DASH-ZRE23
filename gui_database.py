# Database GUI View -----------------------------------------------------------------------------------------------------------
# Author: Cole Barach
# Date Created: 22.01.15
# Date Updated: 23.01.30
#   This module contains all objects related to the Database View of the GUI. The View object may be instanced to create a
#   display for the entire database. This view will display all relevant information from the database.

# Libraries -------------------------------------------------------------------------------------------------------------------
import lib_tkinter
from lib_tkinter import Orientation

# Includes --------------------------------------------------------------------------------------------------------------------
import gui
import config

# Objects ---------------------------------------------------------------------------------------------------------------------
class View(gui.View):
    def __init__(self, parent, id, style, database):
        # Root --------------------------------------------------------------------------------------------------------------------------------------------------------
        super().__init__(parent, id, style, database)

        # Partitioning
        self.root.columnconfigure(0, weight=1) # Center Display
        
        self.root.rowconfigure   (0, weight=1) # Center Display
        self.root.rowconfigure   (1, weight=0) # Button Bar

        # Widgets
        buttonLabels   = ["Back",
                          "",
                          "",
                          ""]
        buttonCommands = [lambda: self.parent.CloseViews(),
                          0,
                          0,
                          0]

        self.displayRoot = lib_tkinter.GetScrollFrame(self.root, column=0, row=0,               sticky="NESW", style=style, orientation=Orientation.VERTICAL)
        self.buttonBar   = lib_tkinter.GetButtonBar  (self.root, column=0, row=1, minHeight=80, sticky="EW",   style=style, orientation=Orientation.HORIZONTAL, commands=buttonCommands, labels=buttonLabels)
        self.display     = self.displayRoot.Get()

        # Display -----------------------------------------------------------------------------------------------------------------------------------------------------
        # Partitioning
        self.display.columnconfigure(0, weight=0) # Labels
        self.display.columnconfigure(1, weight=1) # Stats
        self.display.columnconfigure(2, weight=0) # Labels
        self.display.columnconfigure(3, weight=1) # Stats

        # Widgets
        fontOverride     = [("font", "fontBare")]
        fontBoldOverride = [("font", "fontBareBold")]

        # Communications
        labelCommunications        = lib_tkinter.GetLabel    (self.display, style=style, text="Communications",            column=0, row=0,  sticky="W", styleOverrides=fontBoldOverride)
        ecuCanLabel                = lib_tkinter.GetLabel    (self.display, style=style, text="  ECU CAN Activity:",       column=0, row=1,  sticky="W", styleOverrides=fontOverride)
        acanCanLabel               = lib_tkinter.GetLabel    (self.display, style=style, text="  ACAN CAN Activity:",      column=0, row=2,  sticky="W", styleOverrides=fontOverride)
        bmsCanLabel                = lib_tkinter.GetLabel    (self.display, style=style, text="  BMS CAN Activity:",       column=0, row=3,  sticky="W", styleOverrides=fontOverride)
        inverterCanLabel           = lib_tkinter.GetLabel    (self.display, style=style, text="  Inverter CAN Activity:",  column=0, row=4,  sticky="W", styleOverrides=fontOverride)
        ecuCanTimeLabel            = lib_tkinter.GetLabel    (self.display, style=style, text="  ECU CAN Timeout:",        column=0, row=5,  sticky="W", styleOverrides=fontOverride)
        acanCanTimeLabel           = lib_tkinter.GetLabel    (self.display, style=style, text="  ACAN CAN Timeout:",       column=0, row=6,  sticky="W", styleOverrides=fontOverride)
        bmsCanTimeLabel            = lib_tkinter.GetLabel    (self.display, style=style, text="  BMS CAN Timeout:",        column=0, row=7,  sticky="W", styleOverrides=fontOverride)
        inverterCanTimeLabel       = lib_tkinter.GetLabel    (self.display, style=style, text="  Inverter CAN Timeout:",   column=0, row=8,  sticky="W", styleOverrides=fontOverride)
        self.ecuCanStat            = lib_tkinter.GetCheckStat(self.display, style=style, column=1, row=1, sticky="W",                                   styleOverrides=fontOverride)
        self.acanCanStat           = lib_tkinter.GetCheckStat(self.display, style=style, column=1, row=2, sticky="W",                                   styleOverrides=fontOverride)
        self.bmsCanStat            = lib_tkinter.GetCheckStat(self.display, style=style, column=1, row=3, sticky="W",                                   styleOverrides=fontOverride)
        self.inverterCanStat       = lib_tkinter.GetCheckStat(self.display, style=style, column=1, row=4, sticky="W",                                   styleOverrides=fontOverride)
        self.ecuCanTimeStat        = lib_tkinter.GetLabelStat(self.display, style=style, column=1, row=5, sticky="W", precision=4,                      styleOverrides=fontOverride)
        self.acanCanTimeStat       = lib_tkinter.GetLabelStat(self.display, style=style, column=1, row=6, sticky="W", precision=4,                      styleOverrides=fontOverride)
        self.bmsCanTimeStat        = lib_tkinter.GetLabelStat(self.display, style=style, column=1, row=7, sticky="W", precision=4,                      styleOverrides=fontOverride)
        self.inverterCanTimeStat   = lib_tkinter.GetLabelStat(self.display, style=style, column=1, row=8, sticky="W", precision=4,                      styleOverrides=fontOverride)

        # Pedal Info
        labelPedals                = lib_tkinter.GetLabel    (self.display, style=style, text="Pedal Info",                column=0, row=9,  sticky="W", styleOverrides=fontBoldOverride)
        apps1Label                 = lib_tkinter.GetLabel    (self.display, style=style, text="  APPS-1:",                 column=0, row=10, sticky="W", styleOverrides=fontOverride)
        apps2Label                 = lib_tkinter.GetLabel    (self.display, style=style, text="  APPS-2 Raw:",             column=0, row=11, sticky="W", styleOverrides=fontOverride)
        brake1Label                = lib_tkinter.GetLabel    (self.display, style=style, text="  Brake-1:",                column=0, row=12, sticky="W", styleOverrides=fontOverride)
        brake2Label                = lib_tkinter.GetLabel    (self.display, style=style, text="  Brake-2:",                column=0, row=13, sticky="W", styleOverrides=fontOverride)
        apps1PercentLabel          = lib_tkinter.GetLabel    (self.display, style=style, text="  APPS-1 Percent:",         column=0, row=14, sticky="W", styleOverrides=fontOverride)
        apps2PercentLabel          = lib_tkinter.GetLabel    (self.display, style=style, text="  APPS-2 Percent:",         column=0, row=15, sticky="W", styleOverrides=fontOverride)
        brake1PercentLabel         = lib_tkinter.GetLabel    (self.display, style=style, text="  Brake-1 Percent:",        column=0, row=16, sticky="W", styleOverrides=fontOverride)
        brake2PercentLabel         = lib_tkinter.GetLabel    (self.display, style=style, text="  Brake-2 Percent:",        column=0, row=17, sticky="W", styleOverrides=fontOverride)
        apps1MinLabel              = lib_tkinter.GetLabel    (self.display, style=style, text="  APPS-1 Min:",             column=0, row=18, sticky="W", styleOverrides=fontOverride)
        apps1MaxLabel              = lib_tkinter.GetLabel    (self.display, style=style, text="  APPS-1 Max:",             column=0, row=19, sticky="W", styleOverrides=fontOverride)
        apps2MinLabel              = lib_tkinter.GetLabel    (self.display, style=style, text="  APPS-2 Min:",             column=0, row=20, sticky="W", styleOverrides=fontOverride)
        apps2MaxLabel              = lib_tkinter.GetLabel    (self.display, style=style, text="  APPS-2 Max:",             column=0, row=21, sticky="W", styleOverrides=fontOverride)
        acceleratingLabel          = lib_tkinter.GetLabel    (self.display, style=style, text="  Accelerating:",           column=0, row=22, sticky="W", styleOverrides=fontOverride)
        brakingLabel               = lib_tkinter.GetLabel    (self.display, style=style, text="  Braking:",                column=0, row=23, sticky="W", styleOverrides=fontOverride)
        self.apps1Stat             = lib_tkinter.GetLabelStat(self.display, style=style, column=1, row=10, sticky="W", precision=2,                      styleOverrides=fontOverride)
        self.apps2Stat             = lib_tkinter.GetLabelStat(self.display, style=style, column=1, row=11, sticky="W", precision=2,                      styleOverrides=fontOverride)
        self.brake1Stat            = lib_tkinter.GetLabelStat(self.display, style=style, column=1, row=12, sticky="W", precision=2,                      styleOverrides=fontOverride)
        self.brake2Stat            = lib_tkinter.GetLabelStat(self.display, style=style, column=1, row=13, sticky="W", precision=2,                      styleOverrides=fontOverride)
        self.apps1PercentStat      = lib_tkinter.GetLabelStat(self.display, style=style, column=1, row=14, sticky="W", precision=2,                      styleOverrides=fontOverride)
        self.apps2PercentStat      = lib_tkinter.GetLabelStat(self.display, style=style, column=1, row=15, sticky="W", precision=2,                      styleOverrides=fontOverride)
        self.brake1PercentStat     = lib_tkinter.GetLabelStat(self.display, style=style, column=1, row=16, sticky="W", precision=2,                      styleOverrides=fontOverride)
        self.brake2PercentStat     = lib_tkinter.GetLabelStat(self.display, style=style, column=1, row=17, sticky="W", precision=2,                      styleOverrides=fontOverride)
        self.apps1MinStat          = lib_tkinter.GetLabelStat(self.display, style=style, column=1, row=18, sticky="W", precision=2,                      styleOverrides=fontOverride)
        self.apps1MaxStat          = lib_tkinter.GetLabelStat(self.display, style=style, column=1, row=19, sticky="W", precision=2,                      styleOverrides=fontOverride)
        self.apps2MinStat          = lib_tkinter.GetLabelStat(self.display, style=style, column=1, row=20, sticky="W", precision=2,                      styleOverrides=fontOverride)
        self.apps2MaxStat          = lib_tkinter.GetLabelStat(self.display, style=style, column=1, row=21, sticky="W", precision=2,                      styleOverrides=fontOverride)
        self.acceleratingStat      = lib_tkinter.GetCheckStat(self.display, style=style, column=1, row=22, sticky="W",                                   styleOverrides=fontOverride)
        self.brakingStat           = lib_tkinter.GetCheckStat(self.display, style=style, column=1, row=23, sticky="W",                                   styleOverrides=fontOverride)

        # Motor Data
        labelMotor                 = lib_tkinter.GetLabel    (self.display, style=style, text="Motor Info",                 column=0, row=24, sticky="W", styleOverrides=fontBoldOverride)
        rpmLabel                   = lib_tkinter.GetLabel    (self.display, style=style, text="  Motor RPM:",               column=0, row=25, sticky="W", styleOverrides=fontOverride)
        speedLabel                 = lib_tkinter.GetLabel    (self.display, style=style, text="  Motor Speed:",             column=0, row=26, sticky="W", styleOverrides=fontOverride)
        torquePercentLabel         = lib_tkinter.GetLabel    (self.display, style=style, text="  Torque Percentage Max:",   column=0, row=27, sticky="W", styleOverrides=fontOverride)
        regenPercentLabel          = lib_tkinter.GetLabel    (self.display, style=style, text="  Torque Percentage Regen:", column=0, row=28, sticky="W", styleOverrides=fontOverride)
        motorTempLabel             = lib_tkinter.GetLabel    (self.display, style=style, text="  Motor Temperature:",       column=0, row=29, sticky="W", styleOverrides=fontOverride)
        self.rpmStat               = lib_tkinter.GetLabelStat(self.display, style=style, column=1, row=25, sticky="W", precision=2,                       styleOverrides=fontOverride)
        self.speedStat             = lib_tkinter.GetLabelStat(self.display, style=style, column=1, row=26, sticky="W", precision=2,                       styleOverrides=fontOverride)
        self.torquePercentStat     = lib_tkinter.GetLabelStat(self.display, style=style, column=1, row=27, sticky="W", precision=2,                       styleOverrides=fontOverride)
        self.regenPercentStat      = lib_tkinter.GetLabelStat(self.display, style=style, column=1, row=28, sticky="W", precision=2,                       styleOverrides=fontOverride)
        self.motorTempStat         = lib_tkinter.GetLabelStat(self.display, style=style, column=1, row=29, sticky="W", precision=2,                       styleOverrides=fontOverride)

        # ECU Info
        labelEcu                   = lib_tkinter.GetLabel    (self.display, style=style, text="ECU Info",                  column=2, row=0,  sticky="W", styleOverrides=fontBoldOverride)
        driveStateLabel            = lib_tkinter.GetLabel    (self.display, style=style, text="  Drive State:",            column=2, row=1,  sticky="W", styleOverrides=fontOverride)
        drsStateLabel              = lib_tkinter.GetLabel    (self.display, style=style, text="  DRS State:",              column=2, row=2,  sticky="W", styleOverrides=fontOverride)
        regenStateLabel            = lib_tkinter.GetLabel    (self.display, style=style, text="  Regen State:",            column=2, row=3,  sticky="W", styleOverrides=fontOverride)
        lvBatteryLabel             = lib_tkinter.GetLabel    (self.display, style=style, text="  LV Battery Voltage:",     column=2, row=4,  sticky="W", styleOverrides=fontOverride)
        self.driveStateStat        = lib_tkinter.GetLabelStat(self.display, style=style, column=3, row=1,  sticky="W",                                   styleOverrides=fontOverride)
        self.drsStateStat          = lib_tkinter.GetLabelStat(self.display, style=style, column=3, row=2,  sticky="W",                                   styleOverrides=fontOverride)
        self.regenStateStat        = lib_tkinter.GetLabelStat(self.display, style=style, column=3, row=3,  sticky="W",                                   styleOverrides=fontOverride)
        self.lvBatteryStat         = lib_tkinter.GetLabelStat(self.display, style=style, column=3, row=4,  sticky="W", precision=4,                      styleOverrides=fontOverride)

        # Accumulator Data
        labelAccumulator           = lib_tkinter.GetLabel    (self.display, style=style, text="Accumulator Data",          column=2, row=5,  sticky="W", styleOverrides=fontBoldOverride)
        socLabel                   = lib_tkinter.GetLabel    (self.display, style=style, text="  State of Charge:",        column=2, row=6,  sticky="W", styleOverrides=fontOverride)
        packVoltageLabel           = lib_tkinter.GetLabel    (self.display, style=style, text="  Pack Voltage:",           column=2, row=7,  sticky="W", styleOverrides=fontOverride)
        packCurrentLabel           = lib_tkinter.GetLabel    (self.display, style=style, text="  Pack Current:",           column=2, row=8,  sticky="W", styleOverrides=fontOverride)
        cellVoltageMaxLabel        = lib_tkinter.GetLabel    (self.display, style=style, text="  Cell Voltage Max:",       column=2, row=9,  sticky="W", styleOverrides=fontOverride)
        cellVoltageMinLabel        = lib_tkinter.GetLabel    (self.display, style=style, text="  Cell Voltage Min:",       column=2, row=10, sticky="W", styleOverrides=fontOverride)
        cellDeltaMaxLabel          = lib_tkinter.GetLabel    (self.display, style=style, text="  Cell Delta Max:",         column=2, row=11, sticky="W", styleOverrides=fontOverride)
        cellDeltaMeanLabel         = lib_tkinter.GetLabel    (self.display, style=style, text="  Cell Delta Mean:",        column=2, row=12, sticky="W", styleOverrides=fontOverride)
        packTemperatureMaxLabel    = lib_tkinter.GetLabel    (self.display, style=style, text="  Pack Temperature Max:",   column=2, row=13, sticky="W", styleOverrides=fontOverride)
        packTemperatureMeanLabel   = lib_tkinter.GetLabel    (self.display, style=style, text="  Cell Temperature Mean:",  column=2, row=14, sticky="W", styleOverrides=fontOverride)
        self.socStat               = lib_tkinter.GetLabelStat(self.display, style=style, column=3, row=6,  precision=4,                      sticky="W", styleOverrides=fontOverride)
        self.packVoltageStat       = lib_tkinter.GetLabelStat(self.display, style=style, column=3, row=7,  precision=4,                      sticky="W", styleOverrides=fontOverride)
        self.packCurrentStat       = lib_tkinter.GetLabelStat(self.display, style=style, column=3, row=8,  precision=4,                      sticky="W", styleOverrides=fontOverride)
        self.cellVoltageMaxStat    = lib_tkinter.GetLabelStat(self.display, style=style, column=3, row=9,  precision=4,                      sticky="W", styleOverrides=fontOverride)
        self.cellVoltageMinStat    = lib_tkinter.GetLabelStat(self.display, style=style, column=3, row=10, precision=4,                      sticky="W", styleOverrides=fontOverride)
        self.cellDeltaMax          = lib_tkinter.GetLabelStat(self.display, style=style, column=3, row=11, precision=4,                      sticky="W", styleOverrides=fontOverride)
        self.cellDeltaMean         = lib_tkinter.GetLabelStat(self.display, style=style, column=3, row=12, precision=4,                      sticky="W", styleOverrides=fontOverride)
        self.packTempMaxStat       = lib_tkinter.GetLabelStat(self.display, style=style, column=3, row=13, precision=4,                      sticky="W", styleOverrides=fontOverride)
        self.packTempMeanStat      = lib_tkinter.GetLabelStat(self.display, style=style, column=3, row=14, precision=4,                      sticky="W", styleOverrides=fontOverride)

        # Inverter Info
        labelInverter                = lib_tkinter.GetLabel    (self.display, style=style, text="Inverter Data",                         column=2, row=15, sticky="W", styleOverrides=fontBoldOverride)
        inverterTempGbdLabel         = lib_tkinter.GetLabel    (self.display, style=style, text="  Inv. Temperature Gate Driver Board:", column=2, row=16, sticky="W", styleOverrides=fontOverride)
        inverterTempModuleALabel     = lib_tkinter.GetLabel    (self.display, style=style, text="  Inverter Temperature Module A:",      column=2, row=17, sticky="W", styleOverrides=fontOverride)
        inverterTempModuleBLabel     = lib_tkinter.GetLabel    (self.display, style=style, text="  Inverter Temperature Module B:",      column=2, row=18, sticky="W", styleOverrides=fontOverride)
        inverterTempModuleCLabel     = lib_tkinter.GetLabel    (self.display, style=style, text="  Inverter Temperature Module C:",      column=2, row=19, sticky="W", styleOverrides=fontOverride)
        inverterTempCbLabel          = lib_tkinter.GetLabel    (self.display, style=style, text="  Inverter Temperature Control Board:", column=2, row=20, sticky="W", styleOverrides=fontOverride)
        inverterTempMean             = lib_tkinter.GetLabel    (self.display, style=style, text="  Inverter Mean Temperature:",          column=2, row=21, sticky="W", styleOverrides=fontOverride)
        inverterTempMax              = lib_tkinter.GetLabel    (self.display, style=style, text="  Inverter Max Temperature:",           column=2, row=22, sticky="W", styleOverrides=fontOverride)
        self.inverterTempGdbStat     = lib_tkinter.GetLabelStat(self.display, style=style, column=3, row=16, precision=4,                                  sticky="W", styleOverrides=fontOverride)
        self.inverterTempModuleAStat = lib_tkinter.GetLabelStat(self.display, style=style, column=3, row=17, precision=4,                                  sticky="W", styleOverrides=fontOverride)
        self.inverterTempModuleBStat = lib_tkinter.GetLabelStat(self.display, style=style, column=3, row=18, precision=4,                                  sticky="W", styleOverrides=fontOverride)
        self.inverterTempModuleCStat = lib_tkinter.GetLabelStat(self.display, style=style, column=3, row=19, precision=4,                                  sticky="W", styleOverrides=fontOverride)
        self.inverterTempCbStat      = lib_tkinter.GetLabelStat(self.display, style=style, column=3, row=20, precision=4,                                  sticky="W", styleOverrides=fontOverride)
        self.inverterTempMeanStat    = lib_tkinter.GetLabelStat(self.display, style=style, column=3, row=21, precision=4,                                  sticky="W", styleOverrides=fontOverride)
        self.inverterTempMaxStat     = lib_tkinter.GetLabelStat(self.display, style=style, column=3, row=22, precision=4,                                  sticky="W", styleOverrides=fontOverride)

        # Errors
        labelErrors                  = lib_tkinter.GetLabel    (self.display, style=style, text="Errors",                                column=2, row=23, sticky="W", styleOverrides=fontBoldOverride)
        error25_5Label               = lib_tkinter.GetLabel    (self.display, style=style, text="  Error 25/5 Implausible:",             column=2, row=24, sticky="W", styleOverrides=fontOverride)
        errorInverterFaultLabel      = lib_tkinter.GetLabel    (self.display, style=style, text="  Error Inverter Fault:",               column=2, row=25, sticky="W", styleOverrides=fontOverride)
        errorAcanLabel               = lib_tkinter.GetLabel    (self.display, style=style, text="  Error ACAN Implausible:",             column=2, row=26, sticky="W", styleOverrides=fontOverride)
        error100MsLabel              = lib_tkinter.GetLabel    (self.display, style=style, text="  Error 100ms Implausible:",            column=2, row=27, sticky="W", styleOverrides=fontOverride)
        errorBmsSenseLabel           = lib_tkinter.GetLabel    (self.display, style=style, text="  Error BMS Self Test Fault:",          column=2, row=28, sticky="W", styleOverrides=fontOverride)
        errorBmsTempLabel            = lib_tkinter.GetLabel    (self.display, style=style, text="  Error BMS Temperature Fault:",        column=2, row=29, sticky="W", styleOverrides=fontOverride)
        errorBmsVoltageLabel         = lib_tkinter.GetLabel    (self.display, style=style, text="  Error BMS Voltage Fault:",            column=2, row=30, sticky="W", styleOverrides=fontOverride)
        errorBmsSenseLabel           = lib_tkinter.GetLabel    (self.display, style=style, text="  Error BMS Sense Line Fault:",         column=2, row=31, sticky="W", styleOverrides=fontOverride)
        self.error25_5Stat           = lib_tkinter.GetCheckStat(self.display, style=style, column=3, row=24,                                               sticky="W", styleOverrides=fontOverride)
        self.errorInverterFaultStat  = lib_tkinter.GetCheckStat(self.display, style=style, column=3, row=25,                                               sticky="W", styleOverrides=fontOverride)
        self.errorAcanStat           = lib_tkinter.GetCheckStat(self.display, style=style, column=3, row=26,                                               sticky="W", styleOverrides=fontOverride)
        self.error100MsStat          = lib_tkinter.GetCheckStat(self.display, style=style, column=3, row=27,                                               sticky="W", styleOverrides=fontOverride)
        self.errorBmsSelfStat        = lib_tkinter.GetCheckStat(self.display, style=style, column=3, row=28,                                               sticky="W", styleOverrides=fontOverride)
        self.errorBmsTempStat        = lib_tkinter.GetCheckStat(self.display, style=style, column=3, row=29,                                               sticky="W", styleOverrides=fontOverride)
        self.errorBmsVoltageStat     = lib_tkinter.GetCheckStat(self.display, style=style, column=3, row=30,                                               sticky="W", styleOverrides=fontOverride)
        self.errorBmsSenseStat       = lib_tkinter.GetCheckStat(self.display, style=style, column=3, row=31,                                               sticky="W", styleOverrides=fontOverride)

    def Update(self):
        # Communications
        self.ecuCanStat.Set              (self.database.ecuCanActive)
        self.acanCanStat.Set             (self.database.acanCanActive)
        self.bmsCanStat.Set              (self.database.bmsCanActive)
        self.inverterCanStat.Set         (self.database.inverterCanActive)

        if(self.database.ecuCanTimeout      != None): self.ecuCanTimeStat.Set     (self.database.time - self.database.ecuCanTimeout)
        if(self.database.acanCanTimeout     != None): self.acanCanTimeStat.Set    (self.database.time - self.database.acanCanTimeout)
        if(self.database.bmsCanTimeout      != None): self.bmsCanTimeStat.Set     (self.database.time - self.database.bmsCanTimeout)
        if(self.database.inverterCanTimeout != None): self.inverterCanTimeStat.Set(self.database.time - self.database.inverterCanTimeout)

        # Pedal Info
        self.apps1Stat.Set               (self.database.apps1)
        self.apps2Stat.Set               (self.database.apps2Raw)
        self.brake1Stat.Set              (self.database.brake1)
        self.brake2Stat.Set              (self.database.brake2)
        self.apps1PercentStat.Set        (self.database.apps1Percent)
        self.apps2PercentStat.Set        (self.database.apps2Percent)
        self.brake1PercentStat.Set       (self.database.brake1Percent)
        self.brake2PercentStat.Set       (self.database.brake2Percent)
        self.apps1MinStat.Set            (self.database.apps1Min)
        self.apps1MaxStat.Set            (self.database.apps1Max)
        self.apps2MinStat.Set            (self.database.apps2RawMin)
        self.apps2MaxStat.Set            (self.database.apps2RawMax)
        self.acceleratingStat.Set        (self.database.accelerating)
        self.brakingStat.Set             (self.database.braking)

        # Motor Info
        self.rpmStat.Set                 (self.database.motorRpm)
        self.speedStat.Set               (self.database.motorSpeedMph)
        self.torquePercentStat.Set       (self.database.torquePercentageMax)
        self.regenPercentStat.Set        (self.database.torquePercentageRegen)
        self.motorTempStat.Set           (self.database.motorTemperature)

        # ECU Info
        if(self.database.driveState   == self.database.DriveState.INITIALIZING):
            self.driveStateStat.Set("Initializing...")
        elif(self.database.driveState == self.database.DriveState.LV_DRIVEOFF):
            self.driveStateStat.Set("Low Voltage. Drive OFF")
        elif(self.database.driveState == self.database.DriveState.HV_DRIVEOFF):
            self.driveStateStat.Set("High Voltage. Drive OFF")
        elif(self.database.driveState == self.database.DriveState.HV_DRIVEON):
            self.driveStateStat.Set("High Voltage. Drive ON")
        
        if(self.database.drsState == None):
            self.drsStateStat.Set(None)
        elif(self.database.drsState == True):
            self.drsStateStat.Set("ENABLED")
        elif(self.database.drsState == False):
            self.drsStateStat.Set("DISABLED")

        if(self.database.regenState == None):
            self.regenStateStat.Set(None)
        elif(self.database.regenState == True):
            self.regenStateStat.Set("ENABLED")
        elif(self.database.regenState == False):
            self.regenStateStat.Set("DISABLED")

        self.lvBatteryStat.Set(self.database.lvBatteryVoltage)

        # Accumulator Data
        self.socStat.Set                 (self.database.stateOfCharge)
        self.packVoltageStat.Set         (self.database.packVoltage)
        self.packCurrentStat.Set         (self.database.packCurrent)
        self.cellVoltageMaxStat.Set      (self.database.cellVoltageMax)
        self.cellVoltageMinStat.Set      (self.database.cellVoltageMin)
        self.cellDeltaMax.Set            (self.database.cellDeltaMax)
        self.cellDeltaMean.Set           (self.database.cellDeltaMean)
        self.packTempMaxStat.Set         (self.database.packTemperatureMax)
        self.packTempMeanStat.Set        (self.database.packTemperatureMean)

        # Inverter Data
        self.inverterTempGdbStat.Set     (self.database.inverterTempGdb)
        self.inverterTempModuleAStat.Set (self.database.inverterTempModuleA)
        self.inverterTempModuleBStat.Set (self.database.inverterTempModuleB)
        self.inverterTempModuleCStat.Set (self.database.inverterTempModuleC)
        self.inverterTempCbStat.Set      (self.database.inverterTempCb)
        self.inverterTempMeanStat.Set    (self.database.inverterTempMean)
        self.inverterTempMaxStat.Set     (self.database.inverterTempMax)

        # Errors
        self.error25_5Stat.Set           (self.database.error25_5Implausible)
        self.error100MsStat.Set          (self.database.error100MsImplausible)
        self.errorAcanStat.Set           (self.database.errorAcanImplausible)
        self.errorBmsSelfStat.Set        (self.database.errorBmsSelfTestFault)
        self.errorBmsVoltageStat.Set     (self.database.errorBmsVoltageFault)
        self.errorBmsTempStat.Set        (self.database.errorBmsTempFault)
        self.errorBmsSenseStat.Set       (self.database.errorBmsSenseLineFault)