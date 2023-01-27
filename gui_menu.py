import lib_tkinter
from lib_tkinter import Orientation

import gui

class View(gui.View):
    def __init__(self, parent, id, style, database):
        # Root --------------------------------------------------------------------------------------------------------------------------------------------------------
        super().__init__(parent, id, style, database)

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure   (0, weight=1)

        # Scroll Frame ------------------------------------------------------------------------------------------------------------------------------------------------
        self.scrollFrame = lib_tkinter.GetScrollFrame(self.root, orientation=Orientation.VERTICAL, style=style, column=0, row=0, sticky="NESW")
        self.frame = self.scrollFrame.Get()

        # Partitioning
        self.frame.columnconfigure(0, weight=1) # Left Column
        self.frame.columnconfigure(1, weight=1) # Right Column
        
        # Shortcuts
        self.shortcuts = []

    def AppendShortcut(self, id, icon=None, iconSampling=(1, 1)):
        shortcutCount = len(self.shortcuts)
        rowIndex = int(shortcutCount / 2)
        columnIndex = 0
        if(shortcutCount % 2 == 1):
            columnIndex = 1
        
        command = lambda: self.parent.OpenView(id)

        self.frame.rowconfigure(rowIndex, weight=1)
        shortcut = lib_tkinter.GetImageButton(self.frame, style=self.style, command=command, image=icon, imageSampling=iconSampling, column=columnIndex, row=rowIndex, sticky="NESW")
        self.shortcuts.append(shortcut)