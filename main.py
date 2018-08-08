"""

Title:  Email Breach Checker
Author: Edward Klesel
Date:   30/06/2018

Description:    This program takes a list of email addresses and queries the HaveIBeenPwned API to check if any
                website accounts associated with these email addresses has been breached.

"""

import json
from time import sleep
from Modules import breachHistory
from Classes.cRun import Run
from Modules.breachLogging import breachLog
from Modules.addressChecks import checkAddress, validateAddress

# Load config
with open('Config.json', 'r') as f:
    config = json.loads(f.read())
accounts = config['Accounts']
sleepTime = config['Run']['Sleep Time']

# Start the run
breachLog('info', '***********************************')
breachLog('info', 'Beginning checking Run:')

# Creates a file containing previous breaches, if one doesnt exist
breachHistory.checkFile()

# Creates a Run object
checkingRun = Run()


def main(run):

    breachLog('info', 'Date: ' + str(run.date))
    breachLog('info', 'Time: ' + str(run.time.replace(microsecond=0)))
    numAddresses = len(accounts)
    breachLog('info', 'Checking {} email addresses for new breaches.'.format(numAddresses))

    # Read each email address
    for account in accounts:

        # Extract email address from the configuration
        emailAddress = account['Address']

        # Add in a delay to limit the rate of requests (as per API spec)
        breachLog('debug', 'Sleeping for ' + str(sleepTime) + ' seconds.')
        sleep(sleepTime)
        breachLog('info', '-----------------------------------')

        # Tests the validity of the email address
        breachLog('debug', 'Testing the validity of ' + emailAddress + '.')
        if validateAddress(emailAddress):

            # Email address is valid
            breachLog('debug', emailAddress + ' is a valid email address.')

            # Check the email address for breaches
            checkAddress(account, run)

        # Email address is not valid.
        else:
            breachLog('error', emailAddress + ' is not a valid email address!')

    breachLog('info', '-----------------------------------')
    breachLog('info', 'Checking run finished - {} new breaches detected,'
                      ' {} breaches have updated information.'.format(run.newBreaches, run.amendedBreaches))


if __name__ == '__main__':
    main(checkingRun)
