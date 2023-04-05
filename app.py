# App -------------------------------------------------------------------------------------------------------------------------
# Author: Cole Barach
# Date Created: 22.09.28
# Date Updated: 23.01.30
#   The main file for the application, execute this file to instance the app. This file is responsible for instancing and
#   initializing the CAN and GUI modules.

# Libraries -------------------------------------------------------------------------------------------------------------------
import logging

# Includes --------------------------------------------------------------------------------------------------------------------
import config
import gui
import can_interface
import database

# App Execution ---------------------------------------------------------------------------------------------------------------
if(__name__ == "__main__"):
    # Initialization
    logging.basicConfig(filename=config.LOG_FILE,
                        filemode='w',
                        format="%(asctime)s [%(levelname)s] %(message)s",
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

    try:
        logging.debug("APP - Initializing...")
        mainDatabase = database.Setup()                            # Setup Database
        mainCan      = can_interface.Setup(mainDatabase)           # Setup CAN Interface
        mainGui      = gui.Setup(mainDatabase, mainCan)            # Setup GUI
        
        # Begin
        logging.debug("APP - Begining...")
        mainCan.Begin()                                            # Begin CAN
        mainGui.Begin()                                            # Begin GUI

        # GUI Begin function will not return until app is closed.
        
        # Exit
        logging.debug("APP - Terminating...")
        mainCan.Kill()
        logging.debug("APP - Terminated.")
        logging.shutdown()
        exit()
    except:
        # Exit as Failure
        logging.error("App Failure. Terminating...")
        logging.shutdown()
        exit(1)