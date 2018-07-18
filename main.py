"""

Title:  Email Breach Checker
Author: Edward Klesel
Date:   30/06/2018

Description:    This program takes a list of email addresses and queries the HaveIBeenPwned API to check if any
                website accounts associated with these email addresses has been breached.

"""

import requests
from time import sleep
import breachHistory
from cRun import Run
from breachLogging import breachLog
import re
import sendEmail

# Start the run
breachLog('info','***********************************')
breachLog('info','Beginning checking Run:')

# Creates a file containing previous breaches, if one doesnt exist
breachHistory.checkFile()

checkingRun = Run()

sleepTime = 2


def main(run):

    breachLog('info','Date: ' + str(run.date))
    breachLog('info','Time: ' + str(run.time))
    breachLog('info','Checking {} email addresses for new breaches.'.format(len(open('accounts.txt', 'r').read().splitlines())))

    # Read email accounts from txt file
    with open('accounts.txt', 'r') as emails:

        # Read each email address
        for emailAddress in emails.read().splitlines():

            # Add in a delay to limit the rate of requests (as per API spec)
            breachLog('debug','Sleeping for ' + str(sleepTime) + ' seconds.')
            sleep(sleepTime)

            breachLog('info','-----------------------------------')

            # Tests the validity of the email address
            breachLog('debug','Testing the validity of ' + emailAddress + '.')
            if validateEmail(emailAddress):

                # Email address is valid
                breachLog('debug',emailAddress + ' is a valid email address.')

                # Test the connection to the API
                try:
                    breachLog('info','Checking ' + emailAddress + ' to see if it has been breached...')
                    requests.get('https://haveibeenpwned.com/api/v2/breachedaccount/test@example.com')
                    breachLog('debug','Connection to the HaveIBeenPwned API established.')

                    # Add in a delay to limit the rate of requests (as per API spec)
                    breachLog('debug','Sleeping for ' + str(sleepTime) + ' seconds.')
                    sleep(sleepTime)

                    # If a connection can be established, check the email
                    checkEmail(emailAddress, run)

                # If no connection can be made, catch the error
                except requests.exceptions.ConnectionError as e:
                    breachLog('error','Unable to connect to the HaveIBeenPwned API. See debug log for full error.')
                    breachLog('exception',e)

            # Email address is not valid.
            else:
                breachLog('error',emailAddress + ' is not a valid email address!')

    breachLog('info','-----------------------------------')
    breachLog('info','Checking run finished - {} new breaches detected,'
                      ' {} breaches have updated information.'.format(run.newBreaches, run.amendedBreaches))


def checkEmail(emailAddress, run):

    # Make the GET request
    checkEmail = requests.get('https://haveibeenpwned.com/api/v2/breachedaccount/' + emailAddress)

    newBreachCount = 0

    breachLog('debug','Response code = ' + str(checkEmail.status_code) + ' ' + str(checkEmail.reason))

    # A 200 OK response indicates that the account has been breached
    if checkEmail.status_code == 200:

        # Loads the response from the HaveIBeenPwned API
        breachDetails = checkEmail.json()

        # Loops through each breached site
        for breach in breachDetails:

            newBreach = breachHistory.checkBreach(emailAddress, breach)

            # This breach is not in the list of known breaches
            if newBreach.Write is True:
                newBreachCount += 1
                run.newBreaches += 1

                breachHistory.writeBreach(newBreach)
                sendEmail.sendEmail(newBreach)

                # Presentation function only
                if newBreachCount == 1:
                    breachLog('warning','New breach(es) for ' + emailAddress + ' have been logged! ')

                # Gives the user details of the breach
                breachLog('warning',' ' * 10 + newBreach.Title + ' was breached on '
                                     + newBreach.BreachDate + '!')

            # If this breach is in the list of known breaches, but needs to be updated
            elif newBreach.Amend is True:

                run.amendedBreaches += 1
                breachHistory.amendBreach(newBreach)
                breachLog('debug','newBreachCount = ' + str(newBreachCount))

        # If there are no new breaches, tell the user
        if newBreachCount == 0:
            breachLog('info','The email address ' + emailAddress +
                              ' has not been breached since the last check!')

    # A 404 response indicates the account has not been breached
    elif checkEmail.status_code == 404:
        breachLog('info','The email address ' + emailAddress + ' has not been breached since the last check!')

    # If an unknown response was received from the API
    else:
        breachLog('error','Unable to check ' + emailAddress + ', received a ' + str(checkEmail.status_code) +
                           ' ' + str(checkEmail.reason) + ' response from the HaveIBeenPwned API!')
        breachLog('debug',checkEmail.content)


def validateEmail(address):

    # This searches for emails following the format username@hostname.topleveldomain e.g test@example.com
    format = '[a-zA-Z0-9.]+\@[a-zA-Z0-9]+\.[a-zA-Z]+'
    match = re.search(format, address)

    if match:
        return True
    else:
        return False

if __name__ == '__main__':
    main(checkingRun)
