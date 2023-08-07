# Endurance GUI View ----------------------------------------------------------------------------------------------------------
# Author: Cole Barach
# Date Created: 22.11.23
# Date Updated: 23.04.29
#   This module contains all objects related to the Endurance View of the GUI. The View object may be instanced to create a
#   display for running endurance events.

# Libraries -------------------------------------------------------------------------------------------------------------------
import lib_tkinter
from lib_tkinter import Orientation

# Includes --------------------------------------------------------------------------------------------------------------------
import gui
import gui_speed
import config
import gpio_interface

import logging

# Objects ---------------------------------------------------------------------------------------------------------------------
class View(gui_speed.View):
    def __init__(self, parent, id, style, database):
        super().__init__(parent, id, style, database)

        self.buttonBar.grid_forget()

        buttonLabels   = ["Back",
                          "Speed\nView",
                          "Testing\nView",
                          ""]
        buttonCommands = [lambda: self.parent.CloseViews(),
                          lambda: self.parent.OpenView("Speed"),
                          lambda: self.parent.OpenView("Testing"),
                          0]

        self.buttonBar = lib_tkinter.GetButtonBar(self.root, column=1, row=1, minHeight=style["buttonBarHeight"], sticky="EW", style=style, orientation=Orientation.HORIZONTAL, commands=buttonCommands, labels=buttonLabels)

        self.speedLabel["text"] = "\n\n\n\n SoC"

        self.statPanel.rowconfigure(5, minsize=style["panelStatHeight"])

        self.chargeLabel['text'] = "Acc. Max:"
        self.temp1Label['text']  = "Acc. Mean:"
        self.temp2Label['text']  = "Inv. Max:"
        self.temp3Label['text']  = "Inv. Mean:"
        self.temp4Label = lib_tkinter.GetLabel    (self.statPanel, style=style, column=0, row=5, sticky="W", text="Mtr. Max: ")
        self.temp4Stat  = lib_tkinter.GetLabelStat(self.statPanel, style=style, column=1, row=5, sticky="E", styleOverrides=[("font", "fontLarge")])
    
    def Update(self):
        super().Update()

        self.speedStat.Set(self.database["State_of_Charge"])

        self.chargeStat.Set(self.database["Pack_Temperature_Max"])
        self.temp1Stat.Set(self.database ["Pack_Temperature_Mean"])
        self.temp2Stat.Set(self.database ["Temperature_Inverter_Max"])
        self.temp3Stat.Set(self.database ["Temperature_Inverter_Mean"])
        self.temp4Stat.Set(self.database ["Temperature_Motor"])