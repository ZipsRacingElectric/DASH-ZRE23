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

import logging

# Objects ---------------------------------------------------------------------------------------------------------------------
class View(gui_speed.View):
    def __init__(self, parent, id, style, database):
        super().__init__(parent, id, style, database)

        self.buttonBar.grid_forget()

        buttonLabels   = ["Back",
                          "Speed\nView",
                          "Endurace\nView",
                          ""]
        buttonCommands = [lambda: self.parent.CloseViews(),
                          lambda: self.parent.OpenView("Speed"),
                          lambda: self.parent.OpenView("Endurance"),
                          0]

        self.buttonBar = lib_tkinter.GetButtonBar(self.root, column=1, row=1, minHeight=style["buttonBarHeight"], sticky="EW", style=style, orientation=Orientation.HORIZONTAL, commands=buttonCommands, labels=buttonLabels)

        self.speedStat.grid_forget()
        self.speedLabel.grid_forget()

    def Update(self):
        super().Update()

    def SetDisplayState(self, state):
        super().SetDisplayState("Normal")