# App -------------------------------------------------------------------------------------------------------------------------
# Author: Cole Barach
# Date Created: 22.09.28
# Date Updated: 23.01.30
#   The main file for the application, execute this file to instance the app. This file is responsible for instancing and
#   initializing the CAN and GUI modules.

# Includes --------------------------------------------------------------------------------------------------------------------
import log
from log import print

import gui
import can_interface
import database

# App Execution ---------------------------------------------------------------------------------------------------------------
if(__name__ == "__main__"):
    # Initialization
    log.Setup()

    print("APP - Initializing...")
    mainDatabase = database.Setup()                            # Setup Database
    mainCan      = can_interface.Setup(mainDatabase)           # Setup CAN Interface
    mainGui      = gui.Setup(mainDatabase, mainCan)            # Setup GUI
    
    # Begin
    print("APP - Begining...")
    mainCan.Begin()                                            # Begin CAN
    mainGui.Begin()                                            # Begin GUI

    # GUI Begin function will not return until app is closed.
    
    # Exit
    print("APP - Terminating...")
    mainCan.Kill()
    print("APP - Terminated.")
    print("APP - Closing Log.")
    log.Kill()