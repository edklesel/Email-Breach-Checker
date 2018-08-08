"""

Module: Breach History
Author: Edward Klesel
Date:   08/07/2018

Description:    Module containing methods required for the Email Breach Checker program, which queries the
                HaveIBeenPwned API to check whether accounts created using a given email address have been breached and
                details or the users account leaked.

"""

import os
from Classes.cBreaches import Breach, PastBreach
from Modules.breachLogging import breachLog
import json

# Load config
with open('Config.json', 'r') as f:
    config = json.loads(f.read())

# Define the name/path of the file containing known breaches
knownBreachFile = config['Run']['Known Breaches']


def checkFile():

    """

    Title:  checkFile
    Author: Edward Klesel
    Date:   08/07/2018

    Description:    Checks if a file with a given name exists, and creates it if it does not.

    """

    # Checks if the file already exists
    if not os.path.isfile(knownBreachFile):

        # Creates a new file and writes in the column headers.
        with open(knownBreachFile, 'w') as knownBreaches:
            knownBreaches.write('email,title,breachdate,modifieddate\n')
            breachLog('debug', 'No known breaches found. Creating list of known breaches.')


def checkBreach(address, breach):

    """

    Title:  checkBreach
    Author: Edward Klesel
    Date:   08/07/2018

    Description:    Checks the file containing breaches already known to the user. Returns True if known and False if
                    it's a new breach. Can also check if the breach has been modified and needs amending.


    Arguments:

        address     A simple string containing an email address.

        breach      Information in json format about a given breach for a given email address.

        newBreach   A Breach object which contains information about the breach, whether it is new of not, or whether
                    it needs amending.

    Returns:



    """

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
                    breachLog('debug', 'The ' + newBreach.Title + ' breach on ' + newBreach.BreachDate +
                              ' is already in the list of known breaches.')

                else:
                    breachLog('info', 'There has been an update to the ' + newBreach.Title + ' breach on ' + newBreach.BreachDate + ' since the last check!')
                    newBreach.Amend = True

                # If a matching breach has been found, break the loop
                break

            # The breach has not been seen before
            else:
                newBreach.Write = True
                newBreach.Amend = False

        if newBreach.Write == True:
            breachLog('debug', newBreach.Title + ' is not in the list of known breaches.')

    return newBreach


def writeBreach(newBreach):

    """

    Title:  writeBreach
    Author: Edward Klesel
    Date:   08/07/2018

    Description:    Takes the breach information, formats it and writes it to the file containing known breaches.


    Arguments:

        newBreach   A Breach object containing information about a given breach for a given email address. Used to
                    determine whether the breach needs to be written to file.

    """

    # Writes the new breach to the file containing known breaches
    with open(knownBreachFile, 'a') as knownBreaches:
        knownBreaches.write(newBreach.Info + '\n')
        breachLog('debug', 'Writing ' + newBreach.Title + ' to the list of known breaches.')


def amendBreach(newBreach):

    """

    Title:  amendBreach
    Author: Edward Klesel
    Date:   08/07/2018

    Description:    Takes the breach information, formats it and edits the dateModified in the file containing
                    known breaches to indicate it's been updated.


    Arguments:

        newBreach   A Breach object containing information about a given breach for a given email address. Used to
                    determine whether the breach that is in the file needs to be amended.

    """

    # Reads the list of breaches to memory
    with open(knownBreachFile, 'r') as knownBreachesAll:
        knownBreaches = knownBreachesAll.read().splitlines()

    # Cycles through the list of known breaches until the Core Info matches, then changes the modified date
    with open(knownBreachFile, 'w') as knownBreachesAmend:
        for knownBreach in knownBreaches:

            # If this is the breach which needs amending
            if PastBreach(knownBreach).CoreInfo == newBreach.CoreInfo:
                knownBreachesAmend.write(newBreach.Info + '\n')
                breachLog('debug', 'Amending the ' + newBreach.Title + ' breach on ' + newBreach.BreachDate + '.')
                breachLog('warning', 'The ' + newBreach.Title + ' breach on ' + newBreach.BreachDate + ' has been updated since the last check!')

            # If it's not, don't change anything
            else:
                knownBreachesAmend.write(knownBreach + '\n')
