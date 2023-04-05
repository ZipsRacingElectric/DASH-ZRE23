# Speed GUI View --------------------------------------------------------------------------------------------------------------
# Author: Cole Barach
# Date Created: 22.11.23
# Date Updated: 23.01.30
#   This module contains all objects related to the Speed View of the GUI. The View object may be instanced to create a display
#   for generic driving.

# Libraries -------------------------------------------------------------------------------------------------------------------
import lib_tkinter
from lib_tkinter import Orientation

# Includes --------------------------------------------------------------------------------------------------------------------
import gui
import config

import logging

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
                          "Endurance\nView",
                          "Testing\nView",
                          ""]
        buttonCommands = [lambda: self.parent.CloseViews(),
                          lambda: self.parent.OpenView("Endurance"),
                          lambda: self.parent.OpenView("Testing"),
                          0]

        self.brakeBar   = lib_tkinter.GetProgressBar(self.root, column=0, row=0, minWidth=style["sideBarWidth"], sticky="NS", rowspan=2, style=style, orientation=Orientation.VERTICAL, label="BRAKE",    border=True, scaleFactor=100, styleOverrides=[("lowlight", "accentRed")])
        self.appsBar    = lib_tkinter.GetProgressBar(self.root, column=2, row=0, minWidth=style["sideBarWidth"], sticky="NS", rowspan=2, style=style, orientation=Orientation.VERTICAL, label="THROTTLE", border=True, scaleFactor=100, styleOverrides=[("lowlight", "accentGreen")])
        self.display    = lib_tkinter.GetFrame      (self.root, column=1, row=0, sticky="NESW", style=style, border=True)
        buttonBar       = lib_tkinter.GetButtonBar  (self.root, column=1, row=1, minHeight=style["buttonBarHeight"], sticky="EW", style=style, orientation=Orientation.HORIZONTAL, commands=buttonCommands, labels=buttonLabels)

        self.display.columnconfigure(0, weight=1)
        self.display.rowconfigure   (0, weight=1)

        # Display (Normal) --------------------------------------------------------------------------------------------------------------------------------------------
        self.displayNormal = lib_tkinter.GetFrame(self.display, grid=False, style=style)
        
        # Partitioning
        self.displayNormal.columnconfigure(0, weight=0, minsize=style["statPanelWidth"]) # Stat Panel
        self.displayNormal.columnconfigure(1, weight=1)              # Padding
        self.displayNormal.columnconfigure(2, weight=0)              # Speed Stat
        self.displayNormal.columnconfigure(3, weight=1)              # Padding
        self.displayNormal.columnconfigure(4, weight=0, minsize=style["speedStatWidth"]) # Speed Label

        self.displayNormal.rowconfigure   (0, weight=0) # RPM Panel
        self.displayNormal.rowconfigure   (1, weight=1) # Speed Stat
        self.displayNormal.rowconfigure   (2, weight=0) # Regen Panel 
        self.displayNormal.rowconfigure   (3, weight=0) # Torque Panel

        # Widgets
        rpmPanel       = lib_tkinter.GetFrame       (self.displayNormal, column=0, row=0, style=style, sticky="EW", columnspan=5)
        statPanel      = lib_tkinter.GetFrame       (self.displayNormal, column=0, row=1, style=style, sticky="W")
        speedPanel     = lib_tkinter.GetFrame       (self.displayNormal, column=2, row=1, style=style, sticky="NESW")
        regenPanel     = lib_tkinter.GetFrame       (self.displayNormal, column=0, row=2, style=style, sticky="EW", columnspan=5)
        torquePanel    = lib_tkinter.GetFrame       (self.displayNormal, column=0, row=3, style=style, sticky="EW", columnspan=5)

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
        # Widgets
        self.chargeStat   = lib_tkinter.GetLabelStat(statPanel, style=style, column=1, row=1, sticky="E", styleOverrides=[("font", "fontLarge")])
        self.temp1Stat    = lib_tkinter.GetLabelStat(statPanel, style=style, column=1, row=2, sticky="E", styleOverrides=[("font", "fontLarge")])
        self.temp2Stat    = lib_tkinter.GetLabelStat(statPanel, style=style, column=1, row=3, sticky="E", styleOverrides=[("font", "fontLarge")])
        self.temp3Stat    = lib_tkinter.GetLabelStat(statPanel, style=style, column=1, row=4, sticky="E", styleOverrides=[("font", "fontLarge")], precision=0)
        statDividerTop    = lib_tkinter.GetDivider  (statPanel, style=style, column=0, row=0, sticky="EW", orientation=Orientation.HORIZONTAL, columnspan=2)
        chargeLabel       = lib_tkinter.GetLabel    (statPanel, style=style, column=0, row=1, sticky="W", text="SoC:")
        temp1Label        = lib_tkinter.GetLabel    (statPanel, style=style, column=0, row=2, sticky="W", text="Acc. Max:")
        temp2Label        = lib_tkinter.GetLabel    (statPanel, style=style, column=0, row=3, sticky="W", text="Inv. Max:")
        temp3Label        = lib_tkinter.GetLabel    (statPanel, style=style, column=0, row=4, sticky="W", text="Mtr. Max:")
        statDividerBottom = lib_tkinter.GetDivider  (statPanel, style=style, column=0, row=5, sticky="EW", orientation=Orientation.HORIZONTAL, columnspan=2)

        # Display (Startup) -------------------------------------------------------------------------------------------------------------------------------------------
        self.displayStartup = lib_tkinter.GetFrame(self.display, grid=False, style=style)

        # Partitioning
        self.startupText         = lib_tkinter.GetLabel(self.displayStartup, style=style, column=0, row=0, sticky="EW")
        self.startupInstructions = lib_tkinter.GetLabel(self.displayStartup, style=style, column=0, row=1, sticky="EW")

        self.SetDisplayState("Normal")

    def Update(self):
        if(self.database["State_Ready_to_Drive"] == True):
            self.SetDisplayState("Normal")
        elif(self.database["State_High_Voltage"] == True):
            self.SetDisplayState("Startup_HV")
        elif(self.database["State_High_Voltage"] == False):
            self.SetDisplayState("Startup_LV")
        else:
            self.SetDisplayState("Startup_Invalid")

        self.brakeBar.Set  (self.database["Brake_1_Percent"])
        self.appsBar.Set   (self.database["APPS_1_Percent"])
        self.rpmBar.Set    (self.database["Motor_Speed"])
        # self.torqueBar.Set (self.database[""])
        # self.regenBar.Set  (self.database[""])
        # self.speedStat.Set (self.database[""])
        self.chargeStat.Set(self.database["State_of_Charge"])
        # self.temp1Stat.Set (self.database[""])
        # self.temp2Stat.Set (self.database[""])
        # self.temp3Stat.Set (self.database[""])

    def SetDisplayState(self, state):
        if(state == "Normal"):
            self.displayStartup.forget()
            self.displayNormal.pack()

        elif(state == "Startup_LV"):
            self.displayNormal.forget()
            self.displayStartup.pack()
            
            self.startupText["text"] = "Low Voltage Enabled"
            self.startupInstructions["text"] = "Have an ESO enable tractive systems."
        
        elif(state == "Startup_HV"):
            self.displayNormal.forget()
            self.displayStartup.pack()

            self.startupText["text"] = "High Voltage Enabled"
            self.startupInstructions["text"] = "Press the Brake\nthen the Start Button"

        elif(state == "Startup_Invalid"):
            self.displayNormal.forget()
            self.displayStartup.pack()

            self.startupText["text"] = "ECU Communications Failed"
            self.startupInstructions["text"] = ""