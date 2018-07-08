"""

Title: Breach Logger
Author: Edward Klesel
Date: 08/07/2018

Description:    Module defining the logger used to log events in the Email Breach Checker program.

"""

import logging

logLevel = logging.INFO

def defLog():

    # Give the logger a name so it can be called in other modules.
    breachLogger = logging.getLogger('BreachLogger')

    # Location of the .log file
    logFile = logging.FileHandler('EmailBreachCheck.log')

    # Format of the log entries
    logFormatter = logging.Formatter("%(levelname)-7s - %(asctime)s.%(msecs)03d - %(message)s", '%Y-%m-%d %H:%M:%S')

    # Apply the format to the file
    logFile.setFormatter(logFormatter)

    # Apply the file handler to the logger object
    breachLogger.addHandler(logFile)

    # Set the level of the logging
    breachLogger.setLevel(logLevel)

    return breachLogger