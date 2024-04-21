# Speed GUI View --------------------------------------------------------------------------------------------------------------
# Author: Cole Barach
# Date Created: 22.11.23
# Date Updated: 23.04.29
#   This module contains all objects related to the Speed View of the GUI. The View object may be instanced to create a display
#   for generic driving.

# Libraries -------------------------------------------------------------------------------------------------------------------
import lib_tkinter
from lib_tkinter import Orientation

# Includes --------------------------------------------------------------------------------------------------------------------
import gui
import config
import gpio_interface

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
        self.buttonBar  = lib_tkinter.GetButtonBar  (self.root, column=1, row=1, minHeight=style["buttonBarHeight"], sticky="EW", style=style, orientation=Orientation.HORIZONTAL, commands=buttonCommands, labels=buttonLabels)

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
        self.rpmPanel       = lib_tkinter.GetFrame       (self.displayNormal, column=0, row=0, style=style, sticky="EW", columnspan=5)
        self.statPanel      = lib_tkinter.GetFrame       (self.displayNormal, column=0, row=1, style=style, sticky="W")
        self.speedPanel     = lib_tkinter.GetFrame       (self.displayNormal, column=2, row=1, style=style, sticky="NESW")
        self.regenPanel     = lib_tkinter.GetFrame       (self.displayNormal, column=0, row=2, style=style, sticky="EW", columnspan=5)
        self.torquePanel    = lib_tkinter.GetFrame       (self.displayNormal, column=0, row=3, style=style, sticky="EW", columnspan=5)

        # Speed Panel -------------------------------------------------------------------------------------------------------------------------------------------------
        # Partitioning
        self.speedPanel.columnconfigure(0, weight=0)
        self.speedPanel.columnconfigure(1, weight=0)
        self.speedPanel.rowconfigure(0, weight=1)
        # Widgets
        self.speedStat  = lib_tkinter.GetLabelStat(self.speedPanel, column=0, row=0, style=style, styleOverrides=[("font", "fontExtraLarge")])
        self.speedLabel = lib_tkinter.GetLabel    (self.speedPanel, column=1, row=0, style=style, text="\n\n\n\n MPH", styleOverrides=[("font", "fontLarge")])

        # RPM Panel ---------------------------------------------------------------------------------------------------------------------------------------------------
        # Partitioning
        self.rpmPanel.columnconfigure(0, weight=1)
        # Widgets
        self.rpmBar = lib_tkinter.GetStrataBar(self.rpmPanel, style, Orientation.HORIZONTAL, column=0, row=0, sticky="EW", minHeight=style["rpmBarHeight"], highlights=style["rpmHighlights"], lowlights=style["rpmLowlights"], domain=style["rpmDomain"], mask=style["rpmMask"], scaleFactor=config.RPM_MAX)
        rpmDivider  = lib_tkinter.GetDivider  (self.rpmPanel, style, Orientation.HORIZONTAL, column=0, row=1, sticky="EW")
        
        # Torque Panel ------------------------------------------------------------------------------------------------------------------------------------------------
        # Partitioning
        self.torquePanel.columnconfigure(0, weight=1)
        self.torquePanel.columnconfigure(1, weight=0)
        # Widgets
        self.torqueBar = lib_tkinter.GetProgressBar(self.torquePanel, style, Orientation.HORIZONTAL, minHeight=style["torqueBarHeight"], column=0, row=0, sticky="EW", scaleFactor=config.TORQUE_LIMIT, border=True, styleOverrides=[("lowlight", "accentBlue"), ("borderWidth", "borderWidthLight")])
        torqueLabel    = lib_tkinter.GetLabel      (self.torquePanel, style, column=1, row=0, text="T", styleOverrides=[("font", "fontExtraSmall")])
        
        # Regen Panel -------------------------------------------------------------------------------------------------------------------------------------------------
        # Partitioning
        self.regenPanel.columnconfigure(0, weight=1)
        self.regenPanel.columnconfigure(1, weight=0)
        # Widgets
        self.regenBar = lib_tkinter.GetProgressBar(self.regenPanel, style, Orientation.HORIZONTAL, minHeight=style["torqueBarHeight"], column=0, row=0, sticky="EW", scaleFactor=config.REGEN_LIMIT, border=True, styleOverrides=[("lowlight", "accentGreen"), ("borderWidth", "borderWidthLight")])
        regenLabel    = lib_tkinter.GetLabel      (self.regenPanel, style, column=1, row=0, text="R", styleOverrides=[("font", "fontExtraSmall")])
        
        # Stat Panel --------------------------------------------------------------------------------------------------------------------------------------------------
        # Partitioning
        self.statPanel.columnconfigure(1, minsize=style["panelStatWidth"])
        self.statPanel.rowconfigure   (1, minsize=style["panelStatHeight"])
        self.statPanel.rowconfigure   (2, minsize=style["panelStatHeight"])
        self.statPanel.rowconfigure   (3, minsize=style["panelStatHeight"])
        self.statPanel.rowconfigure   (4, minsize=style["panelStatHeight"])
        # Widgets
        self.chargeStat   = lib_tkinter.GetLabelStat(self.statPanel, style=style, column=1, row=1, sticky="E", styleOverrides=[("font", "fontLarge")])
        self.torqueStat   = lib_tkinter.GetLabelStat(self.statPanel, style=style, column=1, row=2, sticky="E", styleOverrides=[("font", "fontLarge")])
        self.temp2Stat    = lib_tkinter.GetLabelStat(self.statPanel, style=style, column=1, row=3, sticky="E", styleOverrides=[("font", "fontLarge")])
        self.temp3Stat    = lib_tkinter.GetLabelStat(self.statPanel, style=style, column=1, row=4, sticky="E", styleOverrides=[("font", "fontLarge")], precision=0)
        statDividerTop    = lib_tkinter.GetDivider  (self.statPanel, style=style, column=0, row=0, sticky="EW", orientation=Orientation.HORIZONTAL, columnspan=2)
        self.chargeLabel  = lib_tkinter.GetLabel    (self.statPanel, style=style, column=0, row=1, sticky="W", text="SoC:")
        self.torqueLabel  = lib_tkinter.GetLabel    (self.statPanel, style=style, column=0, row=2, sticky="W", text="Torque:")
        self.temp2Label   = lib_tkinter.GetLabel    (self.statPanel, style=style, column=0, row=3, sticky="W", text="Inv. Max:")
        self.temp3Label   = lib_tkinter.GetLabel    (self.statPanel, style=style, column=0, row=4, sticky="W", text="Mtr. Max:")
        statDividerBottom = lib_tkinter.GetDivider  (self.statPanel, style=style, column=0, row=7, sticky="EW", orientation=Orientation.HORIZONTAL, columnspan=2)

        # Display (Startup) -------------------------------------------------------------------------------------------------------------------------------------------
        self.displayStartup = lib_tkinter.GetFrame(self.display, grid=False, style=style)
        
        self.displayStartup.columnconfigure(0, weight=1)
        self.displayStartup.rowconfigure   (0, weight=1)
        self.displayStartup.rowconfigure   (1, weight=1)

        # Partitioning
        self.startupText         = lib_tkinter.GetLabel(self.displayStartup, style=style, column=0, row=0, sticky="EW", styleOverrides=[("font", "fontLarge")])
        self.startupInstructions = lib_tkinter.GetLabel(self.displayStartup, style=style, column=0, row=1, sticky="NEW", styleOverrides=[("font", "fontLarge")])

        self.SetDisplayState("Normal")

    def Update(self):
        # Check for Errors
        #if(self.database["Error_IMD_Fault"] == 1):
        #    self.SetDisplayState("Error_IMD_Fault")

        if(self.database["Error_BMS_Self_Test_Fault"] == 1):
            self.SetDisplayState("Error_BMS_Self_Test_Fault")
            
        elif(self.database["Error_BMS_Sense_Line_Fault"] == 1):
            self.SetDisplayState("Error_BMS_Sense_Line_Fault")
            
        elif(self.database["Error_BMS_Temperature_Fault"] == 1):
            self.SetDisplayState("Error_BMS_Temperature_Fault")
            
        elif(self.database["Error_BMS_Voltage_Fault"] == 1):
            self.SetDisplayState("Error_BMS_Voltage_Fault")
            
        elif(self.database["Plausibility_APPS_Calibration"] == 0):
            self.SetDisplayState("Error_APPS_Calibration")
            
        elif(self.database["Plausibility_Brakes_Calibration"] == 0):
            self.SetDisplayState("Error_Brakes_Calibration")
            
        elif(self.database["Plausibility_Pedals"] == 0):
            self.SetDisplayState("Error_Plausibility_Pedals")
        
        elif(self.database["Error_BSPD_Fault"] == 1):
            self.SetDisplayState("Error_BSPD_Fault")
            
        elif(self.database["Plausibility_APPS_25_5"] == 0):
            self.SetDisplayState("Error_APPS_25_5")

        # Determine Drive State
        elif(self.database["State_Ready_to_Drive"] == True and self.database["ECU_CAN_Active"]):
            self.SetDisplayState("Normal")

        elif(self.database["State_High_Voltage"] == True and self.database["ECU_CAN_Active"]):
            self.SetDisplayState("Startup_HV")

        elif(self.database["State_High_Voltage"] == False and self.database["ECU_CAN_Active"]):
            self.SetDisplayState("Startup_LV")

        else:
            self.SetDisplayState("Startup_Invalid")

        self.brakeBar.Set  (self.database["Brake_1_Percent"])
        self.appsBar.Set   (self.database["APPS_1_Percent"])
        self.rpmBar.Set    (self.database["Motor_Speed"])
        self.torqueBar.Set (self.database["Torque_Config_Limit"])
        self.regenBar.Set  (self.database["Torque_Config_Limit_Regen"])
        self.speedStat.Set (self.database["Motor_Speed_MPH"])
        self.chargeStat.Set(self.database["State_of_Charge"])
        if(self.database["Torque_Config_Limit"] != None): self.torqueStat.Set(int(self.database["Torque_Config_Limit"] / 2.3))
        self.temp2Stat.Set (self.database["Temperature_Inverter_Max"])
        self.temp3Stat.Set (self.database["Temperature_Motor"])

        if(self.database["State_Regen_Config_Enabled"] == True):
            self.regenBar.SetColor(self.style["accentGreen"])
        else:
            self.regenBar.SetColor(self.style["lowlightGreen"])

    def SetDisplayState(self, state):
        if(state == "Normal"):
            self.displayStartup.grid_forget()
            self.displayNormal.grid(column=0, row=0, sticky="NESW")
            gpio_interface.SetRgb(config.GPIO_RGB_PIN_R, False, False, False, -1)

        elif(state == "Startup_LV"):
            self.displayNormal.grid_forget()
            self.displayStartup.grid(column=0, row=0, sticky="NESW")
            
            self.startupText["text"] = "Low Voltage Enabled"
            self.startupInstructions["text"] = "When ready, an ESO will\nenable tractive systems."
            gpio_interface.SetRgb(config.GPIO_RGB_PIN_R, False, True, False, -1)
        
        elif(state == "Startup_HV"):
            self.displayNormal.grid_forget()
            self.displayStartup.grid(column=0, row=0, sticky="NESW")

            self.startupText["text"] = "Tractive Systems Enabled"
            self.startupInstructions["text"] = "To enter drive mode,\npress and hold the brake\nthen press the start button."
            gpio_interface.SetRgb(config.GPIO_RGB_PIN_R, True, False, False, -1)

        elif(state == "Startup_Invalid"):
            self.displayNormal.grid_forget()
            self.displayStartup.grid(column=0, row=0, sticky="NESW")

            self.startupText["text"] = "ECU Communications Failed"
            self.startupInstructions["text"] = "If the ECU is online, the\nECU Status Message (0x703)\nhas not been recieved."
            gpio_interface.SetRgb(config.GPIO_RGB_PIN_R, False, False, True, -1)

        elif(state == "Error_BSPD_Fault"):
            self.displayNormal.grid_forget()
            self.displayStartup.grid(column=0, row=0, sticky="NESW")

            self.startupText["text"] = "BPSD Fault"
            self.startupInstructions["text"] = "Please have an ESO\nreset the vehicle."
            gpio_interface.SetRgb(config.GPIO_RGB_PIN_R, False, False, True, -1)

        elif(state == "Error_APPS_25_5"):
            self.displayNormal.grid_forget()
            self.displayStartup.grid(column=0, row=0, sticky="NESW")

            self.startupText["text"] = "APPS 25/5 Implausibility"
            self.startupInstructions["text"] = "Release the throttle fully\nand continue driving!"
            gpio_interface.SetRgb(config.GPIO_RGB_PIN_R, True, True, False, -1)

        elif(state == "Error_Plausibility_Pedals"):
            self.displayNormal.grid_forget()
            self.displayStartup.grid(column=0, row=0, sticky="NESW")

            self.startupText["text"] = "Pedal Value Implausibility"
            self.startupInstructions["text"] = "Release both pedals fully.\nIf the error persists,\nrecalibrate the pedals."
            gpio_interface.SetRgb(config.GPIO_RGB_PIN_R, True, True, False, -1)

        elif(state == "Error_APPS_Calibration"):
            self.displayNormal.grid_forget()
            self.displayStartup.grid(column=0, row=0, sticky="NESW")

            self.startupText["text"] = "APPS Calibration Implausibility"
            self.startupInstructions["text"] = "Recalibrate the pedals.\nIf the error persists,\nmaintenance is required."
            gpio_interface.SetRgb(config.GPIO_RGB_PIN_R, False, False, True, -1)

        elif(state == "Error_Brakes_Calibration"):
            self.displayNormal.grid_forget()
            self.displayStartup.grid(column=0, row=0, sticky="NESW")

            self.startupText["text"] = "Brake Calibration Implausibility"
            self.startupInstructions["text"] = "Recalibrate the pedals.\nIf the error persists,\nmaintenance is required."
            gpio_interface.SetRgb(config.GPIO_RGB_PIN_R, False, False, True, -1)

        #elif(state == "Error_IMD_Fault"):
                #self.displayNormal.grid_forget()
                #self.displayStartup.grid(column=0, row=0, sticky="NESW")
#
                #self.startupText["text"] = "WARNING: IMD Fault"
                #self.startupInstructions["text"] = "Exit the vehicle immediately."
                #gpio_interface.SetRgb(config.GPIO_RGB_PIN_R, True, False, False, 0.1)

        elif(state == "Error_BMS_Self_Test_Fault"):
            self.displayNormal.grid_forget()
            self.displayStartup.grid(column=0, row=0, sticky="NESW")

            self.startupText["text"] = "WARNING: Accumulator Fault"
            self.startupInstructions["text"] = "Exit the vehicle immediately."
            gpio_interface.SetRgb(config.GPIO_RGB_PIN_R, True, False, False, 0.1)

        elif(state == "Error_BMS_Sense_Line_Fault"):
            self.displayNormal.grid_forget()
            self.displayStartup.grid(column=0, row=0, sticky="NESW")

            self.startupText["text"] = "WARNING: Accumulator Fault"
            self.startupInstructions["text"] = "Exit the vehicle immediately."
            gpio_interface.SetRgb(config.GPIO_RGB_PIN_R, True, False, False, 0.1)

        elif(state == "Error_BMS_Temperature_Fault"):
            self.displayNormal.grid_forget()
            self.displayStartup.grid(column=0, row=0, sticky="NESW")

            self.startupText["text"] = "WARNING: Accumulator Fault"
            self.startupInstructions["text"] = "Exit the vehicle immediately."
            gpio_interface.SetRgb(config.GPIO_RGB_PIN_R, True, False, False, 0.1)

        elif(state == "Error_BMS_Voltage_Fault"):
            self.displayNormal.grid_forget()
            self.displayStartup.grid(column=0, row=0, sticky="NESW")

            self.startupText["text"] = "WARNING: Accumulator Fault"
            self.startupInstructions["text"] = "Exit the vehicle immediately."
            gpio_interface.SetRgb(config.GPIO_RGB_PIN_R, True, False, False, 0.1)