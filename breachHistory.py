"""

Module: Breach History
Author: Edward Klesel
Date:   08/07/2018

Description:    Module containing methods required for the Email Breach Checker program, which queries the HaveIBeenPwned API
                to check whether accounts created using a given email address have been breached and details leaked.

Methods:

checkFile    -  Checks if a file with a given name exists, and creates it if it does not.

checkBreach  -  Checks the file containing breaches already known to the user. Returns True if known and False if it's a
                new breach. Can also check if the breach has been modified and needs amending (True/False).

writeBreach  -  Takes the breach information, formats it and writes it to the file containing known breaches.

amendBreach  -  Takes the breach information, formats it and edits the dateModified in the file containing Known Breaches
                to indicate it's been updated.

"""

import breachLogging
import os
from Breaches import Breach, PastBreach
import logging

# Enables log entries to be written
breachLogger = logging.getLogger('BreachLogger')

# Define the name/path of the file containing known breaches
knownBreachFile = 'KnownBreaches.csv'

def checkFile():

    # Checks if the file already exists
    if not os.path.isfile(knownBreachFile):

        # Creates a new file and writes in the column headers.
        with open(knownBreachFile, 'w') as knownBreaches:
            knownBreaches.write('email,title,breachdate,modifieddate\n')
            breachLogger.debug('No known breaches found. Creating list of known breaches.')


def checkBreach(address, breach):

    # Creates a new Breach object
    newBreach = Breach(address, breach)

    # Opens the history file in read mode
    with open(knownBreachFile, 'r') as knownBreaches:

        for knownBreach in knownBreaches.read().splitlines():

            # Creates an object representing the past breach
            pastBreach = PastBreach(knownBreach)

            # Checks if this breach is already known to have happened
            if pastBreach.CoreInfo == newBreach.CoreInfo:

                # This is not a new breach
                newBreach.Write = False

                # Checks if the breach has been updated since the last check
                if pastBreach.ModifiedDate == newBreach.ModifiedDate:

                    # This breach is unchanged since the last check
                    newBreach.Amend = False
                    breachLogger.debug('The ' + newBreach.Title + ' breach on ' + newBreach.BreachDate + ' is already in the list of known breaches.')

                else:
                    breachLogger.info('There has been an update to the ' + newBreach.Title + ' breach on ' + newBreach.BreachDate + ' since the last check!')
                    newBreach.Amend = True

                # If a matching breach has been found, break the loop
                break

            # The breach has not been seen before
            else:
                newBreach.Write = True
                newBreach.Amend = False

        if newBreach.Write == True:
            breachLogger.debug(newBreach.Title + ' is not in the list of known breaches.')

    return newBreach

def writeBreach(newBreach):

    # Writes the new breach to the file containing known breaches
    with open(knownBreachFile, 'a') as knownBreaches:
        knownBreaches.write(newBreach.Info + '\n')
        breachLogger.debug('Writing ' + newBreach.Title + ' to the list of known breaches.')

def amendBreach(newBreach):

    # Reads the list of breaches to memory
    with open(knownBreachFile, 'r') as knownBreachesAll:
        knownBreaches = knownBreachesAll.read().splitlines()

    # Cycles through the list of known breaches until the Core Info matches, then changes the modified date
    with open(knownBreachFile, 'w') as knownBreachesAmend:
        for knownBreach in knownBreaches:

            # If this is the breach which needs amending
            if PastBreach(knownBreach).CoreInfo == newBreach.CoreInfo:
                knownBreachesAmend.write(newBreach.Info + '\n')
                breachLogger.debug('Amending the ' + newBreach.Title + ' breach on ' + newBreach.BreachDate + '.')
                breachLogger.warning('The ' + newBreach.Title + ' breach on ' + newBreach.BreachDate + ' has been updated since the last check!')

            # If it's not, don't change anything
            else:
                knownBreachesAmend.write(knownBreach + '\n')
