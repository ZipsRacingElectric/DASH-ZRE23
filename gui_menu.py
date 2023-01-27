import lib_tkinter
from lib_tkinter import Orientation

import gui

class View(gui.View):
    def __init__(self, parent, id, style, database):
        # Root --------------------------------------------------------------------------------------------------------------------------------------------------------
        super().__init__(parent, id, style, database)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure   (0, weight=1)

        self.scrollOffset = 0

        # Partitioning
        self.root.columnconfigure(0, weight=1) # Left Column
        self.root.columnconfigure(1, weight=1) # Right Column
        self.root.rowconfigure   (0, weight=1) # Top Row
        self.root.rowconfigure   (1, weight=1) # Bottom Row
        
        self.scrollUp   = lib_tkinter.GetButton(self.root, style, lambda: self.Scroll(1),  "    \u25B2    ", column=2, row=0, sticky="NESW", styleOverrides=[("font", "fontLarge")])
        self.scrollDown = lib_tkinter.GetButton(self.root, style, lambda: self.Scroll(-1), "    \u25BC    ", column=2, row=1, sticky="NESW", styleOverrides=[("font", "fontLarge")])

        # Shortcuts
        self.shortcuts = []

    def Scroll(self, scroll):
        self.scrollOffset -= scroll*2
        
        shortcutCount = len(self.shortcuts)
        if(self.scrollOffset > shortcutCount - 4): self.scrollOffset = shortcutCount - 4
        if(self.scrollOffset < 0): self.scrollOffset = 0 

        for shortcut in self.shortcuts:
            shortcut[0].grid_forget()

        if(self.scrollOffset >= shortcutCount): return
        self.shortcuts[self.scrollOffset][0].grid  (column=0, row=0, sticky="NESW")
        if(self.scrollOffset+1 >= shortcutCount): return
        self.shortcuts[self.scrollOffset+1][0].grid(column=1, row=0, sticky="NESW")
        if(self.scrollOffset+2 >= shortcutCount): return
        self.shortcuts[self.scrollOffset+2][0].grid(column=0, row=1, sticky="NESW")
        if(self.scrollOffset+3 >= shortcutCount): return
        self.shortcuts[self.scrollOffset+3][0].grid(column=1, row=1, sticky="NESW")

    def AppendShortcut(self, id, icon=None, iconSampling=(1, 1)):
        command = lambda: self.parent.OpenView(id)

        shortcut = lib_tkinter.GetImageButton(self.root, style=self.style, command=command, image=icon, imageSampling=iconSampling, sticky="NESW")
        self.shortcuts.append(shortcut)

        self.Scroll(0)