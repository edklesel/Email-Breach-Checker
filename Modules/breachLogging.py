"""

Title:  breachLogging
Author: Edward Klesel
Date:   10/07/2018

Description:    Module containing the functions used to log in multiple log files
                at different logging levels from one function call.

"""

import logging
import datetime
import os
import json

# Setting up the dates used for the folders/files
today = datetime.date.today()
year = str(today.year)
month = str(today.month)
day = str(today.day)
if len(month) == 1:
    month = '0' + month
if len(day) == 1:
    day = '0' + day
fileDate = year + '-' + month + '-' + day
folderDate = year + '-' + month

# Load Config
with open('Config.json', 'r') as f:
    config = json.loads(f.read())
logDir = config['Logging']['Location']

# Check that a folder for this month exists
if not os.path.isdir(logDir):
    os.mkdir(logDir)
if not os.path.isdir(logDir + '/' + folderDate):
    os.mkdir(logDir + '/' + folderDate)

# Giving the loggers two unique identities
breachLogger = logging.getLogger('BreachLogger')
breachLoggerDebug = logging.getLogger('BreachLoggerDebug')

# The file locations of the main log file and the debug log file
logMain = logging.FileHandler('logs/' + folderDate + '/' + fileDate + '_EmailBreachCheck.log', "a",
                              encoding="UTF-8")
logDebug = logging.FileHandler('logs/' + folderDate + '/' + fileDate + '_EmailBreachCheck_Debug.log', "a",
                               encoding="UTF-8")

# Both loggers use the same format, so only one formatter is needed
logFormatter = logging.Formatter(config['Logging']['Format'], config['Logging']['Date Format'])
logMain.setFormatter(logFormatter)
logDebug.setFormatter(logFormatter)

# Adding the associated handlers to the logger
breachLogger.addHandler(logMain)
breachLoggerDebug.addHandler(logDebug)

# Setting the level of the different loggers
breachLogger.setLevel(logging.INFO)
breachLoggerDebug.setLevel(logging.DEBUG)


def breachLog(level, message):

    """

    Title:  breachLog
    Author: Edward Klesel
    Date:   10/07/2018

    Description:    Logs entries at a specified level in different log files. File-names are specified at the start
                    of the module.


    Arguments:

        level       The level of log message to be written.

        message     The log entry which is to be written to the log file.

    """

    # For debug messages, only log to the debug logger
    if level.lower() == 'debug':
        breachLoggerDebug.debug(message)

    # For all else, log to both
    elif level.lower() == 'info':
        breachLogger.info(message)
        breachLoggerDebug.info(message)

    elif level.lower() == 'error':
        breachLogger.error(message)
        breachLoggerDebug.error(message)

    elif level.lower() == 'warning':
        breachLogger.warning(message)
        breachLoggerDebug.warning(message)

    elif level.lower() == 'critical':
        breachLogger.critical(message)
        breachLoggerDebug.critical(message)

    elif level.lower() == 'exception':
        breachLogger.exception(message)
        breachLoggerDebug.exception(message)