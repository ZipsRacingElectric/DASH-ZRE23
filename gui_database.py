# Database GUI View -----------------------------------------------------------------------------------------------------------
# Author: Cole Barach
# Date Created: 22.01.15
# Date Updated: 23.01.30
#   This module contains all objects related to the Database View of the GUI. The View object may be instanced to create a
#   display for the entire database. This view will display all relevant information from the database.

# Libraries -------------------------------------------------------------------------------------------------------------------
import lib_tkinter
from lib_tkinter import Orientation

import math

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
        self.display.columnconfigure(0, weight=1) # Labels
        self.display.columnconfigure(1, weight=1) # Stats
        self.display.columnconfigure(2, weight=1) # Units
        # self.display.columnconfigure(3, weight=1) # Comment

        # Widgets
        fontOverride     = [("font", "fontBare")]
        fontBoldOverride = [("font", "fontBareBold")]

        self.stats = dict()
        messages = database.db.messages

        # Pack Widgets
        renderedKeys = []
        
        row = 0
        for message in messages:
            if("Cell_Voltages" in message.name): return
            if("Cell_Balancings" in message.name): return
            if("Pack_Temperatures" in message.name): return

            lib_tkinter.GetLabel(self.display, style=style, text=f"{message.name} ({hex(message.frame_id)}): ", column=0, row=row, sticky="W", styleOverrides=fontBoldOverride)
            row += 1

            signals = message.signals
            for signal in signals:
                lib_tkinter.GetLabel(self.display, style=style, text=f"  {signal.name}: ", column=0, row=row, sticky="W", styleOverrides=fontOverride)

                if(signal.unit == "Boolean"):
                    self.stats[signal.name] = lib_tkinter.GetCheckStat(self.display, style=style, column=1, row=row, sticky="W", styleOverrides=fontOverride)
                else:
                    self.stats[signal.name] = lib_tkinter.GetLabelStat(self.display, style=style, column=1, row=row, sticky="W", precision=4, styleOverrides=fontOverride)

                lib_tkinter.GetLabel(self.display, style=style, text=f"Unit: {signal.unit}", column=2, row=row, sticky="W", styleOverrides=fontOverride)

                row += 1
                renderedKeys.append(signal.name)

        lib_tkinter.GetLabel(self.display, style=style, text=f"Extrapolated: ", column=0, row=row, sticky="W", styleOverrides=fontBoldOverride)
        row += 1

        for key, value in self.database.items():
            if(key == "db" or key == "overrides"): continue

            keyIsRendered = False
            for renderedKey in renderedKeys:
                if(key == renderedKey): keyIsRendered = True

            if(not keyIsRendered):
                lib_tkinter.GetLabel(self.display, style=style, text=f"  {key}: ", column=0, row=row, sticky="W", styleOverrides=fontOverride)
                self.stats[key] = lib_tkinter.GetLabelStat(self.display, style=style, column=1, row=row, sticky="W", precision=4, styleOverrides=fontOverride)
                row += 1

    def Update(self):
        index = 0

        messages = self.database.db.messages
        for key, value in self.stats.items():
            self.stats[key].Set(self.database[key])