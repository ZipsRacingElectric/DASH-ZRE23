# Log -------------------------------------------------------------------------------------------------------------------------
# Author: Cole Barach
# Date Created: 23.04.01
# Date Updated: 23.04.01
#   The main logger for the application.

import os
import config

def Setup():
    global mainLog

    parentPath = os.path.dirname(__file__)
    logPath    = os.path.join(parentPath, config.LOG_FILE)

    mainLog = open(logPath, "w")

def Kill():
    global mainLog
    mainLog.close()

def print(text):
    global mainLog
    mainLog.write(text + "\n")