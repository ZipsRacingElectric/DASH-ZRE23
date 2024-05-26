# Testing GUI View ------------------------------------------------------------------------------------------------------------
# Author: Cole Barach
# Date Created: 22.01.31
# Date Updated: 23.01.31

# Libraries -------------------------------------------------------------------------------------------------------------------
import lib_tkinter
from lib_tkinter import Orientation

# Includes --------------------------------------------------------------------------------------------------------------------
import gui
import gui_speed
import config
import gpio_interface
import can_interface

import logging

# Objects ---------------------------------------------------------------------------------------------------------------------
class View(gui_speed.View):
    def __init__(self, parent, id, style, database, can_t):
        super().__init__(parent, id, style, database)

        self.can_transmitter = can_t
        self.database = database

        self.buttonBar.grid_forget()

        buttonLabels   = ["Back",
                          "+ Torque",
                          "- Torque",
                          ""]
        buttonCommands = [lambda: self.parent.CloseViews(),
                          lambda: self.TorqueUp(),
                          lambda: self.TorqueDown(),
                          0]

        self.buttonBar = lib_tkinter.GetButtonBar(self.root, column=1, row=1, minHeight=style["buttonBarHeight"], sticky="EW", style=style, orientation=Orientation.HORIZONTAL, commands=buttonCommands, labels=buttonLabels)

        self.speedStat.grid_forget()
        self.speedLabel.grid_forget()

    def Update(self):
        super().Update()

    def SetDisplayState(self, state):
        super().SetDisplayState("Normal")

    def TorqueUp(self):
        if(self.database["Torque_Config_Limit"] == None): return

        if(self.database["Torque_Config_Limit"] > 230): return
        
        self.database["Torque_Config_Limit"] = self.database["Torque_Config_Limit"] + 11

        self.database["Torque_Config_Limit_Regen"] = 0
        self.database["State_Regen_Config_Enabled"] = False

        can_interface.SendCommandDriveConfiguration(self.can_transmitter, self.database)

    def TorqueDown(self):
        print(self.database["Torque_Config_Limit"])

        if(self.database["Torque_Config_Limit"] == None): return
        
        if(self.database["Torque_Config_Limit"] < 11): return
        
        self.database["Torque_Config_Limit"] = self.database["Torque_Config_Limit"] - 11

        self.database["Torque_Config_Limit_Regen"] = 0
        self.database["State_Regen_Config_Enabled"] = False

        can_interface.SendCommandDriveConfiguration(self.can_transmitter, self.database)
