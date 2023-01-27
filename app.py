import gui
import can_interface
import database

class App():
    def __init__(self):
        print("APP - Initializing...")
        self.database = database.Setup()
        self.can = can_interface.Setup(self.database)
        self.gui = gui.Setup(self.database)
        
    def Begin(self):
        print("APP - Begining...")
        self.can.Begin()
        self.gui.Begin()

    def Kill(self):
        print("APP - Terminating...")
        self.can.Kill()
        print("APP - Terminated.")

if(__name__ == "__main__"):
    app = App()
    app.Begin()
    app.Kill()