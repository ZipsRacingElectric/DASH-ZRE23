import gui
import appCan
import database

class App():
    def __init__(self):
        print("APP - Initializing...")
        self.database = database.Setup()
        self.can = appCan.Setup(self.database)
        self.gui = gui.Setup(self.database)
         
    def Begin(self):
        print("APP - Begining...")
        self.can.Begin()
        self.gui.Begin()

    def Kill(self):
        self.can.Kill()
        print("APP - Terminated.")

if(__name__ == "__main__"):
    app = App()
    app.Begin()
    app.Kill()