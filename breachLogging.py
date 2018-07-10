"""

Title:  breachMultiLogging
Author: Edward Klesel
Date:   10/07/2018

Description:    Module containing the functions used to log in multiple log files
                at different logging levels from one function call.

Functions:

breachLog - Logs entries at a specified level in different log files. Filenames
            are specified at the start of the module.

"""

import logging

# Giving the loggers two unique identities
breachLogger = logging.getLogger('BreachLogger')
breachLoggerDebug = logging.getLogger('BreachLoggerDebug')

# The file locations of the main log file and the debug log file
logMain = logging.FileHandler('EmailBreachCheck.log')
logDebug = logging.FileHandler('EmailBreachCheck_Debug.log')

# Both loggers use the same format, so only one formatter is needed
logFormatter = logging.Formatter("%(levelname)-7s - %(asctime)s.%(msecs)03d - %(message)s", '%Y-%m-%d %H:%M:%S')
logMain.setFormatter(logFormatter)
logDebug.setFormatter(logFormatter)

# Adding the associated handlers to the logger
breachLogger.addHandler(logMain)
breachLoggerDebug.addHandler(logDebug)

# Setting the level of the different loggers
breachLogger.setLevel(logging.INFO)
breachLoggerDebug.setLevel(logging.DEBUG)

def breachLog(level, message):

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