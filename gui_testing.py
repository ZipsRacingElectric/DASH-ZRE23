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
    def __init__(self, parent, id, style, database):
        super().__init__(parent, id, style, database)

        self.buttonBar.grid_forget()

        buttonLabels   = ["Back",
                          "Speed\nView",
                          "Torque Down",
                          "Torque Upies"]
        buttonCommands = [lambda: self.parent.CloseViews(),
                          lambda: self.parent.OpenView("Speed"),
                          lambda: self.torqueDown(),
                          lambda: self.torqueUpies()
                          ,]

        self.buttonBar = lib_tkinter.GetButtonBar(self.root, column=1, row=1, minHeight=style["buttonBarHeight"], sticky="EW", style=style, orientation=Orientation.HORIZONTAL, commands=buttonCommands, labels=buttonLabels)

        self.speedStat.grid_forget()
        self.speedLabel.grid_forget()

    def torqueUpies(self):
        self.database["Torque_Config_Limit"] += 5
        can_interface.SendCommandDriveConfiguration()

    def torqueDown(self):
        self.database["Torque_Config_Limit"] -= 5
        can_interface.SendCommandDriveConfiguration()
        

    def Update(self):
        super().Update()

    def SetDisplayState(self, state):
        super().SetDisplayState("Normal")