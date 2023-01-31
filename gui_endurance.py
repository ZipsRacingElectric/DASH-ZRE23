# Endurance GUI View ----------------------------------------------------------------------------------------------------------
# Author: Cole Barach
# Date Created: 22.11.23
# Date Updated: 23.01.30
#   This module contains all objects related to the Endurance View of the GUI. The View object may be instanced to create a
#   display for running endurance events.

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
        self.root.columnconfigure(0, weight=0) # Brake Bar
        self.root.columnconfigure(1, weight=1) # Center Display
        self.root.columnconfigure(2, weight=0) # APPS Bar

        self.root.rowconfigure   (0, weight=1) # Center Display
        self.root.rowconfigure   (1, weight=0) # Button Bar

        # Widgets
        buttonLabels   = ["Back",
                          "Testing\nView",
                          "Speed\nView",
                          ""]
        buttonCommands = [lambda: self.parent.CloseViews(),
                          lambda: self.parent.OpenView("Testing"),
                          lambda: self.parent.OpenView("Speed"),
                          0]

        self.brakeBar   = lib_tkinter.GetProgressBar(self.root, column=0, row=0, minWidth=style["sideBarWidth"], sticky="NS", rowspan=2, style=style, orientation=Orientation.VERTICAL, label="BRAKE",    border=True, scaleFactor=100, styleOverrides=[("lowlight", "accentRed")])
        self.appsBar    = lib_tkinter.GetProgressBar(self.root, column=2, row=0, minWidth=style["sideBarWidth"], sticky="NS", rowspan=2, style=style, orientation=Orientation.VERTICAL, label="THROTTLE", border=True, scaleFactor=100, styleOverrides=[("lowlight", "accentGreen")])
        self.display    = lib_tkinter.GetFrame      (self.root, column=1, row=0, sticky="NESW", style=style, border=True)
        buttonBar       = lib_tkinter.GetButtonBar  (self.root, column=1, row=1, minHeight=style["buttonBarHeight"], sticky="EW", style=style, orientation=Orientation.HORIZONTAL, commands=buttonCommands, labels=buttonLabels)

        # Display -----------------------------------------------------------------------------------------------------------------------------------------------------
        # Partitioning
        self.display.columnconfigure(0, weight=0, minsize=style["statPanelWidth"]) # Stat Panel
        self.display.columnconfigure(1, weight=1)              # Padding
        self.display.columnconfigure(2, weight=0)              # Speed Stat
        self.display.columnconfigure(3, weight=1)              # Padding
        self.display.columnconfigure(4, weight=0, minsize=style["speedStatWidth"]) # Speed Label

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

        # Charge Panel ------------------------------------------------------------------------------------------------------------------------------------------------
        # Partitioning
        speedPanel.columnconfigure(0, weight=0)
        speedPanel.columnconfigure(1, weight=0)
        speedPanel.rowconfigure(0, weight=1)
        # Widgets
        self.chargeStat = lib_tkinter.GetLabelStat(speedPanel, column=0, row=0, style=style, styleOverrides=[("font", "fontExtraLarge")])
        chargeLabel     = lib_tkinter.GetLabel    (speedPanel, column=1, row=0, style=style, text="\n\n\n\n SoC", styleOverrides=[("font", "fontLarge")])

        # RPM Panel ---------------------------------------------------------------------------------------------------------------------------------------------------
        # Partitioning
        rpmPanel.columnconfigure(0, weight=1)
        # Widgets
        self.rpmBar = lib_tkinter.GetStrataBar(rpmPanel, style, Orientation.HORIZONTAL, column=0, row=0, sticky="EW", minHeight=style["rpmBarHeight"], highlights=style["rpmHighlights"], lowlights=style["rpmLowlights"], domain=style["rpmDomain"], mask=style["rpmMask"], scaleFactor=config.RPM_MAX)
        rpmDivider  = lib_tkinter.GetDivider  (rpmPanel, style, Orientation.HORIZONTAL, column=0, row=1, sticky="EW")
        
        # Torque Panel ------------------------------------------------------------------------------------------------------------------------------------------------
        # Partitioning
        torquePanel.columnconfigure(0, weight=1)
        torquePanel.columnconfigure(1, weight=0)
        # Widgets
        self.torqueBar = lib_tkinter.GetProgressBar(torquePanel, style, Orientation.HORIZONTAL, minHeight=style["torqueBarHeight"], column=0, row=0, sticky="EW", scaleFactor=100, border=True, styleOverrides=[("lowlight", "accentBlue"), ("borderWidth", "borderWidthLight")])
        torqueLabel    = lib_tkinter.GetLabel      (torquePanel, style, column=1, row=0, text="T", styleOverrides=[("font", "fontExtraSmall")])
        
        # Regen Panel -------------------------------------------------------------------------------------------------------------------------------------------------
        # Partitioning
        regenPanel.columnconfigure(0, weight=1)
        regenPanel.columnconfigure(1, weight=0)
        # Widgets
        self.regenBar = lib_tkinter.GetProgressBar(regenPanel, style, Orientation.HORIZONTAL, minHeight=style["torqueBarHeight"], column=0, row=0, sticky="EW", scaleFactor=100, border=True, styleOverrides=[("lowlight", "accentGreen"), ("borderWidth", "borderWidthLight")])
        regenLabel    = lib_tkinter.GetLabel      (regenPanel, style, column=1, row=0, text="R", styleOverrides=[("font", "fontExtraSmall")])
        
        # Stat Panel --------------------------------------------------------------------------------------------------------------------------------------------------
        # Partitioning
        statPanel.columnconfigure(1, minsize=style["panelStatWidth"])
        statPanel.rowconfigure   (1, minsize=style["panelStatHeight"])
        statPanel.rowconfigure   (2, minsize=style["panelStatHeight"])
        statPanel.rowconfigure   (3, minsize=style["panelStatHeight"])
        statPanel.rowconfigure   (4, minsize=style["panelStatHeight"])
        statPanel.rowconfigure   (5, minsize=style["panelStatHeight"])
        # Widgets
        self.temp1Stat    = lib_tkinter.GetLabelStat(statPanel, style=style, column=1, row=1, sticky="E", styleOverrides=[("font", "fontLarge")])
        self.temp2Stat    = lib_tkinter.GetLabelStat(statPanel, style=style, column=1, row=2, sticky="E", styleOverrides=[("font", "fontLarge")])
        self.temp3Stat    = lib_tkinter.GetLabelStat(statPanel, style=style, column=1, row=3, sticky="E", styleOverrides=[("font", "fontLarge")])
        self.temp4Stat    = lib_tkinter.GetLabelStat(statPanel, style=style, column=1, row=4, sticky="E", styleOverrides=[("font", "fontLarge")])
        self.temp5Stat    = lib_tkinter.GetLabelStat(statPanel, style=style, column=1, row=5, sticky="E", styleOverrides=[("font", "fontLarge")])
        statDividerTop    = lib_tkinter.GetDivider  (statPanel, style=style, column=0, row=0, sticky="EW", orientation=Orientation.HORIZONTAL, columnspan=2)
        temp1Label        = lib_tkinter.GetLabel    (statPanel, style=style, column=0, row=1, sticky="W", text="Acc. Max:")
        temp2Label        = lib_tkinter.GetLabel    (statPanel, style=style, column=0, row=2, sticky="W", text="Acc. Avg:")
        temp3Label        = lib_tkinter.GetLabel    (statPanel, style=style, column=0, row=3, sticky="W", text="Inv. Max:")
        temp4Label        = lib_tkinter.GetLabel    (statPanel, style=style, column=0, row=4, sticky="W", text="Inv. Avg:")
        temp5Label        = lib_tkinter.GetLabel    (statPanel, style=style, column=0, row=5, sticky="W", text="Mtr. Avg:")
        statDividerBottom = lib_tkinter.GetDivider  (statPanel, style=style, column=0, row=6, sticky="EW", orientation=Orientation.HORIZONTAL, columnspan=2)

    def Update(self):
        self.brakeBar.Set  (self.database.brake1Percent)
        self.appsBar.Set   (self.database.apps1Percent)
        self.rpmBar.Set    (self.database.motorRpm)
        self.torqueBar.Set (self.database.torquePercentageMax)
        self.regenBar.Set  (self.database.torquePercentageRegen)
        self.chargeStat.Set(self.database.stateOfCharge)
        self.temp1Stat.Set (self.database.packTemperatureMax)
        self.temp2Stat.Set (self.database.packTemperatureMean)
        self.temp3Stat.Set (self.database.inverterTempMax)
        self.temp4Stat.Set (self.database.inverterTempMean)
        self.temp5Stat.Set (self.database.motorTemperature)