import lib_tkinter
from lib_tkinter import Orientation

import gui
import config

class View(gui.View):
    def __init__(self, parent, id, style, database):
        # Root --------------------------------------------------------------------------------------------------------------------------------------------------------
        super().__init__(parent, id, style, database)

        # Partitioning
        self.root.columnconfigure(0, weight=0) # Brake Bar
        self.root.columnconfigure(1, weight=1) # Center Display
        self.root.columnconfigure(2, weight=0) # APPS Bar

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

        self.brakeBar   = lib_tkinter.GetProgressBar(self.root, column=0, row=0, minWidth=70, sticky="NS", rowspan=2, style=style, orientation=Orientation.VERTICAL, label="BRAKE",    border=True, scaleFactor=100, styleOverrides=[("lowlight", "accentRed")])
        self.appsBar    = lib_tkinter.GetProgressBar(self.root, column=2, row=0, minWidth=70, sticky="NS", rowspan=2, style=style, orientation=Orientation.VERTICAL, label="THROTTLE", border=True, scaleFactor=100, styleOverrides=[("lowlight", "accentGreen")])
        self.display    = lib_tkinter.GetFrame      (self.root, column=1, row=0, sticky="NESW", style=style, border=True)
        buttonBar       = lib_tkinter.GetButtonBar  (self.root, column=1, row=1, minHeight=80, sticky="EW", style=style, orientation=Orientation.HORIZONTAL, commands=buttonCommands, labels=buttonLabels)

        # Display -----------------------------------------------------------------------------------------------------------------------------------------------------
        # Partitioning
        self.display.columnconfigure(0, weight=0, minsize=224) # Stat Panel
        self.display.columnconfigure(1, weight=1)              # Padding
        self.display.columnconfigure(2, weight=0)              # Speed Stat
        self.display.columnconfigure(3, weight=1)              # Padding
        self.display.columnconfigure(4, weight=0, minsize=160) # Speed Label

        self.display.rowconfigure   (0, weight=0) # RPM Panel
        self.display.rowconfigure   (1, weight=1) # Speed Stat
        self.display.rowconfigure   (2, weight=0) # Regen Panel 
        self.display.rowconfigure   (3, weight=0) # Torque Panel

        # Widgets
        rpmPanel       = lib_tkinter.GetFrame       (self.display, column=0, row=0, style=style, sticky="EW", columnspan=5)
        statPanel      = lib_tkinter.GetFrame       (self.display, column=0, row=1, style=style, sticky="W")
        speedPanel     = lib_tkinter.GetFrame       (self.display, column=2, row=1, style=style, sticky="NESW")
        regenPanel     = lib_tkinter.GetFrame       (self.display, column=0, row=2, style=style, sticky="EW", columnspan=5)
        torquePanel    = lib_tkinter.GetFrame       (self.display, column=0, row=3, style=style, sticky="EW", columnspan=5)

        # Speed Panel -------------------------------------------------------------------------------------------------------------------------------------------------
        # Partitioning
        speedPanel.columnconfigure(0, weight=0)
        speedPanel.columnconfigure(1, weight=0)
        speedPanel.rowconfigure(0, weight=1)
        # Widgets
        self.speedStat = lib_tkinter.GetLabelStat(speedPanel, column=0, row=0, style=style, styleOverrides=[("font", "fontExtraLarge")])
        speedLabel     = lib_tkinter.GetLabel    (speedPanel, column=1, row=0, style=style, text="\n\n\n\n MPH", styleOverrides=[("font", "fontLarge")])

        # RPM Panel ---------------------------------------------------------------------------------------------------------------------------------------------------
        # Partitioning
        rpmPanel.columnconfigure(0, weight=1)
        # Widgets
        self.rpmBar = lib_tkinter.GetStrataBar(rpmPanel, style, Orientation.HORIZONTAL, column=0, row=0, sticky="EW", minHeight=100, highlights=style["rpmHighlights"], lowlights=style["rpmLowlights"], domain=style["rpmDomain"], mask=style["rpmMask"], scaleFactor=config.RPM_MAX)
        rpmDivider  = lib_tkinter.GetDivider  (rpmPanel, style, Orientation.HORIZONTAL, column=0, row=1, sticky="EW")
        
        # Torque Panel ------------------------------------------------------------------------------------------------------------------------------------------------
        # Partitioning
        torquePanel.columnconfigure(0, weight=1)
        torquePanel.columnconfigure(1, weight=0)
        # Widgets
        self.torqueBar = lib_tkinter.GetProgressBar(torquePanel, style, Orientation.HORIZONTAL, minHeight=8, column=0, row=0, sticky="EW", scaleFactor=100, border=True, styleOverrides=[("lowlight", "accentBlue"), ("borderWidth", "borderWidthLight")])
        torqueLabel    = lib_tkinter.GetLabel      (torquePanel, style, column=1, row=0, text="T", styleOverrides=[("font", "fontExtraSmall")])
        
        # Regen Panel -------------------------------------------------------------------------------------------------------------------------------------------------
        # Partitioning
        regenPanel.columnconfigure(0, weight=1)
        regenPanel.columnconfigure(1, weight=0)
        # Widgets
        self.regenBar = lib_tkinter.GetProgressBar(regenPanel, style, Orientation.HORIZONTAL, minHeight=8, column=0, row=0, sticky="EW", scaleFactor=100, border=True, styleOverrides=[("lowlight", "accentGreen"), ("borderWidth", "borderWidthLight")])
        regenLabel    = lib_tkinter.GetLabel      (regenPanel, style, column=1, row=0, text="R", styleOverrides=[("font", "fontExtraSmall")])
        
        # Stat Panel --------------------------------------------------------------------------------------------------------------------------------------------------
        # Partitioning
        statPanel.columnconfigure(1, minsize=80)
        statPanel.rowconfigure   (1, minsize=50)
        statPanel.rowconfigure   (2, minsize=50)
        statPanel.rowconfigure   (3, minsize=50)
        # Widgets
        self.chargeStat   = lib_tkinter.GetLabelStat(statPanel, style=style, column=1, row=1, sticky="E", styleOverrides=[("font", "fontLarge")])
        self.temp1Stat    = lib_tkinter.GetLabelStat(statPanel, style=style, column=1, row=2, sticky="E", styleOverrides=[("font", "fontLarge")])
        self.temp2Stat    = lib_tkinter.GetLabelStat(statPanel, style=style, column=1, row=3, sticky="E", styleOverrides=[("font", "fontLarge")])
        self.temp3Stat    = lib_tkinter.GetLabelStat(statPanel, style=style, column=1, row=4, sticky="E", styleOverrides=[("font", "fontLarge")])
        statDividerTop    = lib_tkinter.GetDivider  (statPanel, style=style, column=0, row=0, sticky="EW", orientation=Orientation.HORIZONTAL, columnspan=2)
        chargeLabel       = lib_tkinter.GetLabel    (statPanel, style=style, column=0, row=1, sticky="W", text="SoC:")
        temp1Label        = lib_tkinter.GetLabel    (statPanel, style=style, column=0, row=2, sticky="W", text="Acc. Max:")
        temp2Label        = lib_tkinter.GetLabel    (statPanel, style=style, column=0, row=3, sticky="W", text="Inv. Max:")
        temp3Label        = lib_tkinter.GetLabel    (statPanel, style=style, column=0, row=4, sticky="W", text="Mtr. Max:")
        statDividerBottom = lib_tkinter.GetDivider  (statPanel, style=style, column=0, row=5, sticky="EW", orientation=Orientation.HORIZONTAL, columnspan=2)

    def Update(self):
        self.brakeBar.Set  (self.database.brake1Percent)
        self.appsBar.Set   (self.database.apps1Percent)
        self.rpmBar.Set    (self.database.motorRpm)
        self.torqueBar.Set (self.database.torquePercentageMax)
        self.regenBar.Set  (self.database.torquePercentageRegen)
        self.speedStat.Set (self.database.motorSpeedMph)
        self.chargeStat.Set(self.database.stateOfCharge)
        self.temp1Stat.Set (self.database.packTemperatureMax)
        self.temp2Stat.Set (self.database.inverterTempMax)
        self.temp3Stat.Set (self.database.motorTemperature)