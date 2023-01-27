# Libraries
import tkinter

# Objects
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

# Imports
import lib_tkinter
import gui_menu
import gui_speed
import gui_endurance
import gui_testing
import gui_database
import gui_bms
import gui_calibration
import gui_debug

FRAMERATE = 32

def Setup(database):
    # Instance GUI
    gui = Main("Dashboard 2023 - Rev.2", database, FRAMERATE)
    gui.geometry('1024x600')

    # Import Styles
    dash  = lib_tkinter.Style("style_Dash.json")
    debug = lib_tkinter.Style("style_Debug.json")
    
    # Instance Views
    menu = gui_menu.View(gui, id="Menu", style=dash, database=database)
    gui.AppendView(menu)
    gui.AppendView(gui_speed.View      (gui, id="Speed",       style=dash, database=database))
    gui.AppendView(gui_endurance.View  (gui, id="Endurance",   style=dash, database=database))
    gui.AppendView(gui_testing.View    (gui, id="Testing",     style=dash, database=database))
    gui.AppendView(gui_bms.View        (gui, id="Bms",         style=dash, database=database))
    gui.AppendView(gui_calibration.View(gui, id="Calibration", style=dash, database=database))
    gui.AppendView(gui_database.View   (gui, id="Database",    style=dash, database=database))

    # Setup Menu
    menu.AppendShortcut(id="Speed",       icon=r'./icons/Speed.png',       iconSampling=(0.5, 0.5))
    menu.AppendShortcut(id="Endurance",   icon=r'./icons/Endurance.png',   iconSampling=(0.5, 0.5))
    menu.AppendShortcut(id="Testing",     icon=r'./icons/Testing.png',     iconSampling=(0.5, 0.5))
    menu.AppendShortcut(id="Bms",         icon=r'./icons/Bms.png',         iconSampling=(0.5, 0.5))
    menu.AppendShortcut(id="Calibration", icon=r'./icons/Calibration.png', iconSampling=(0.5, 0.5))
    menu.AppendShortcut(id="Database",    icon=r'./icons/Database.png',    iconSampling=(0.5, 0.5))
    
    # Open Menu
    gui.CloseViews()

    # Instance Sub-Windows
    gui.AppendWindow(gui_debug.Window(gui, id="Debug", style=debug))
    
    # Setup Keybinds
    gui.AppendKeybind("F2", lambda: gui.ToggleWindow("Debug"))

    return gui

class Main(tkinter.Tk):
    def __init__(self, title, database, framerate=0):
        print("GUI - Initializing...")
        super().__init__()

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
