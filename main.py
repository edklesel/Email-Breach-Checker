import requests
import json
from time import sleep
import breachLogging
import breachHistory

# Define logger
breachLogger = breachLogging.defLog()

# Start the run
breachLogger.info('-----------------------------------')
breachLogger.info('Beginning checking Run:')


# Creates a file containing previous breaches, if one doesnt exist
breachHistory.checkFile()


def main():

    newBreachesTotal = 0
    amendedBreachesTotal = 0

    # Read email accounts from txt file
    with open('accounts.txt', 'r') as t:

        # Read each email address
        for emailAddress in t.read().splitlines():

            # Make the GET request
            checkEmail = requests.get('https://haveibeenpwned.com/api/v2/breachedaccount/' + emailAddress)
            breachLogger.info('Checking ' + emailAddress + ' to see if it has been breached...')

            newBreachCount = 0

            breachLogger.debug('Response code = ' + str(checkEmail.status_code) + ' ' + str(checkEmail.reason))

            # A 200 OK response indicates that the account has been breached
            if checkEmail.status_code == 200:

                # Loads the response from the HaveIBeenPwned API
                breachDetails = json.loads(checkEmail.content)

                # Loops through each breached site
                for breach in breachDetails:

                    newBreach = breachHistory.checkBreach(emailAddress, breach)

                    # This breach is not in the list of known breaches
                    if newBreach.Write is True:
                        newBreachCount += 1
                        newBreachesTotal += 1

                        breachHistory.writeBreach(newBreach)

                        # Presentation function only
                        if newBreachCount == 1:
                            breachLogger.warning('New breach(es) for ' + emailAddress + ' have been logged! ')

                        # Gives the user details of the breach
                        breachLogger.warning(' '*10 + newBreach.Title + ' was breached on '
                                             + newBreach.BreachDate + '!')

                    # If this breach is in the list of known breaches, but needs to be updated
                    elif newBreach.Amend is True:
                        amendedBreachesTotal += 1
                        breachHistory.amendBreach(newBreach)

                breachLogger.debug('newBreachCount = '  + str(newBreachCount))

                # If there are no new breaches, tell the user
                if newBreachCount == 0:
                    breachLogger.info('The email address ' + emailAddress +
                                      ' has not been breached since the last check!')

            # A 404 response indicates the account has not been breached
            elif checkEmail.status_code == 404:
                breachLogger.info('The email address ' + emailAddress + ' has not been breached since the last check!')

            # If an unknown response was received from the API
            else:
                breachLogger.error('Unable to check ' + emailAddress + ', received a ' + str(checkEmail.status_code) +
                                   ' ' + str(checkEmail.reason) + ' response from the HaveIBeenPwned API!')
                breachLogger.debug(checkEmail.content)

            # Add in a delay to limit the rate of requests (as per API spec)
            sleepTime = 2
            breachLogger.debug('Sleeping for ' + str(sleepTime) + ' seconds.')
            sleep(sleepTime)

    breachLogger.info('Checking run finished - {} new breaches detected,'
                      ' {} breaches have updated information.'.format(newBreachesTotal, amendedBreachesTotal))


try:
    requests.get('https://haveibeenpwned.com/api/v2/breachedaccount/test@example.com')
    breachLogger.debug('Connection to the HaveIBeenPwned API established.')
    runCode = True
except requests.exceptions.ConnectionError as e:
    breachLogger.error('Unable to connect to the HaveIBeenPwned API. Full error below:')
    breachLogger.error(e)
    runCode = False

if __name__ == '__main__' and runCode is True:
    main()
