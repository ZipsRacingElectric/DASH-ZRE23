# GUI -------------------------------------------------------------------------------------------------------------------------
# Author: Cole Barach
# Date Created: 22.11.23
# Date Updated: 23.01.30
#   This module contains all code related to the GUI. Instancing the Main object of this script will create a TK window, which
#   may have views, windows, and interrupts appended as necessary. Any GUI Views and Windows should inherit from the
#   respective objects in this script. Call setup to get a configured and initialized Main object.

# Libraries -------------------------------------------------------------------------------------------------------------------
import tkinter
import lib_tkinter

import os
import inspect

# Objects ---------------------------------------------------------------------------------------------------------------------
class View():
    def __init__(self, parent, id, style, database):
        self.parent   = parent
        self.id       = id
        self.style    = style
        self.database = database
        
        self.root   = lib_tkinter.GetFrame(parent, style, grid=False)
        self.open   = False

    def Open(self):
        self.root.pack(expand=True, fill="both")
        self.open = True

    def Close(self):
        self.root.forget()
        self.open = False

    def Update(self):
        return

class Window():
    def __init__(self, parent, id, style):
        self.parent = parent
        self.id     = id
        self.style  = style
        self.open   = False

    def Open(self):
        self.root = tkinter.Toplevel(self.parent)
        self.open = True

    def Close(self):
        self.root.destroy()
        self.open = False

    def Toggle(self):
        if(self.open):
            self.Close()
        else:
            self.Open()

# Imports ---------------------------------------------------------------------------------------------------------------------
import config

# Views
import gui_menu
import gui_speed
import gui_endurance
import gui_testing
import gui_database
import gui_bms
import gui_calibration
import gui_debug

# Functions -------------------------------------------------------------------------------------------------------------------
def Setup(database, can):
    # Instance GUI
    gui = Main("Dashboard 2023 - Rev.2", database, config.GUI_FRAMERATE)
    gui.geometry(f'{config.GUI_WIDTH}x{config.GUI_HEIGHT}')
    gui.SetFullscreen(True)

    parentPath = os.path.dirname(__file__)

    # Import Styles
    dashStylePath  = os.path.join(parentPath, config.GUI_DASH_STYLE)
    debugStylePath = os.path.join(parentPath, config.GUI_DEBUG_STYLE)
    
    dashStyle  = lib_tkinter.Style(dashStylePath)
    debugStyle = lib_tkinter.Style(debugStylePath)
    
    # Instance Views
    menu = gui_menu.View(gui, id="Menu", style=dashStyle, database=database)
    gui.AppendView(menu)
    gui.AppendView(gui_speed.View      (gui, id="Speed",       style=dashStyle, database=database))
    gui.AppendView(gui_endurance.View  (gui, id="Endurance",   style=dashStyle, database=database))
    gui.AppendView(gui_testing.View    (gui, id="Testing",     style=dashStyle, database=database))
    gui.AppendView(gui_bms.View        (gui, id="Bms",         style=dashStyle, database=database))
    gui.AppendView(gui_calibration.View(gui, id="Calibration", style=dashStyle, databaseObj=database, canTransmitter=can))
    gui.AppendView(gui_database.View   (gui, id="Database",    style=dashStyle, database=database))


    # Setup Menu
    iconSpeedPath       = os.path.join(parentPath, config.ICON_SPEED)
    iconEndurancePath   = os.path.join(parentPath, config.ICON_ENDURANCE)
    iconTestingPath     = os.path.join(parentPath, config.ICON_TESTING)
    iconBmsPath         = os.path.join(parentPath, config.ICON_BMS)
    iconCalibrationPath = os.path.join(parentPath, config.ICON_CALIBRATION)
    iconDatabasePath    = os.path.join(parentPath, config.ICON_DATABASE)
    
    iconSampling = (config.ICON_SCALING, config.ICON_SCALING)
    
    menu.AppendShortcut(id="Speed",       icon=iconSpeedPath,       iconSampling=iconSampling)
    menu.AppendShortcut(id="Endurance",   icon=iconEndurancePath,   iconSampling=iconSampling)
    menu.AppendShortcut(id="Testing",     icon=iconTestingPath,     iconSampling=iconSampling)
    menu.AppendShortcut(id="Bms",         icon=iconBmsPath,         iconSampling=iconSampling)
    menu.AppendShortcut(id="Calibration", icon=iconCalibrationPath, iconSampling=iconSampling)
    menu.AppendShortcut(id="Database",    icon=iconDatabasePath,    iconSampling=iconSampling)
    
    # Open Menu
    gui.CloseViews()

    # Instance Sub-Windows
    gui.AppendWindow(gui_debug.Window(gui, id="Debug", style=debugStyle, can=can))
    
    # Setup Keybinds
    gui.AppendKeybind("F2", lambda: gui.ToggleWindow("Debug"))
    gui.AppendKeybind("F1", lambda: gui.ToggleFullscreen())

    return gui

# GUI Object ------------------------------------------------------------------------------------------------------------------
class Main(tkinter.Tk):
    def __init__(self, title, database, framerate=0):
        print("GUI - Initializing...")
        super().__init__()

        self.SetFullscreen(False)

        self.title(title)

        self.database = database

        self.InitializeViews()
        self.InitializeWindows()
        self.InitializeKeybinds()

        self.framerate = framerate

        print("GUI - Initialized.")

    # Views -----------------------------------------------------------------------------------
    def InitializeViews(self):
        self.views = []
        self.activeView = None

    def AppendView(self, view):
        self.views.append(view)

    def OpenView(self, view):
        # Open by ID
        if(type(view) == type("")):
            viewId = view
            view = None
            for targetView in self.views:
                if(targetView.id == viewId):
                    view = targetView
                    break
            if(view == None):
                print("GUI - Could not find view of ID '" + viewId + "'")
                return
        
        # Open by Reference
        if(issubclass(type(view), View)):
            self.CloseViews(openDefaultView=False)
            view.Open()
            self.activeView = view
            return

        # Invalid Object
        print("GUI - Object '" + str(type(view)) + "' must inherit from 'gui.View")

    def CloseViews(self, openDefaultView=True):
        self.activeView = None
        for view in self.views:
            view.Close()
        if(openDefaultView):
            self.views[0].Open()
            self.activeView = self.views[0]

    # Windows ---------------------------------------------------------------------------------
    def InitializeWindows(self):
        self.windows = []

    def AppendWindow(self, window):
        self.windows.append(window)

    def ToggleWindow(self, window):
        # Open by ID
        if(type(window) == type("")):
            windowId = window
            window = None
            for targetWindow in self.windows:
                if(targetWindow.id == windowId):
                    window = targetWindow
                    break
            if(window == None):
                print("GUI - Could not find window of ID '" + windowId + "'")
                return
        
        # Open by Reference
        if(issubclass(type(window), Window)):
            window.Toggle()
            return

        # Invalid Object
        print("GUI - Object '" + str(type(window)) + "' must inherit from 'gui.View")

    # Keybinds --------------------------------------------------------------------------------
    def InitializeKeybinds(self):
        self.bind('<Key>', self.KeybindInterrupt)
        self.keybindValues   = []
        self.keybindCommands = []

    def AppendKeybind(self, key, command):
        self.keybindValues.append(key)
        self.keybindCommands.append(command)

    def KeybindInterrupt(self, event):
        for index in range(len(self.keybindValues)):
            if(event.keysym == self.keybindValues[index]): self.keybindCommands[index]()

    def SetFullscreen(self, fullscreen):
        self.fullscreen = fullscreen
        self.attributes("-fullscreen", fullscreen)

    def ToggleFullscreen(self):
        self.fullscreen = not self.fullscreen
        self.SetFullscreen(self.fullscreen)

    # Behavior --------------------------------------------------------------------------------
    def Update(self):
        if(self.activeView != None):
            self.activeView.Update()

    def Loop(self):
        if(self.framerate == 0 or self.framerate == None): return
        delayMilliseconds = int(1000 / self.framerate)
        
        self.Update()
        self.after(delayMilliseconds, self.Loop)

    def Begin(self):
        print("GUI - Loop Starting...")
        self.Loop()
        self.mainloop()
        print("GUI - Loop Terminated.")

    def Kill(self):
        if(self.state != 'normal'): return
        self.destroy()
