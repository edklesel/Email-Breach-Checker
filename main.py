import requests
import json
import os
import logging
from time import sleep
from iso8601 import parse_date

# Define logger
breachLogger = logging.getLogger('breachLogger')
logFile = logging.FileHandler('EmailBreachCheck.log')
logFormatter = logging.Formatter("%(levelname)-7s - %(asctime)s.%(msecs)03d - %(message)s", '%Y-%m-%d %H:%M:%S')
logFile.setFormatter(logFormatter)
logFile.setLevel(logging.DEBUG)
breachLogger.addHandler(logFile)

# Turn debugging on?
debug = 0

# Set Logging Level
if debug == 0:
    breachLogger.setLevel(logging.INFO)
elif debug == 1:
    breachLogger.setLevel(logging.DEBUG)

#Start the run
breachLogger.info('-----------------------------------')
breachLogger.info('Beginning checking Run:')

newBreachesTotal = 0
amendedBreachesTotal = 0

# Creates a file containing previous breaches, if one doesnt exist
if not os.path.isfile('KnownBreaches.csv'):
    with open('KnownBreaches.csv', 'w') as knownBreaches:
        knownBreaches.write('email,title,breachdate,modifieddate\n')
        breachLogger.debug('No known breaches found. Creating list of known breaches.')

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

                breachTitle = breach['Title']
                breachDate = breach['BreachDate']
                breachModified = str(parse_date(breach['ModifiedDate']).date())

                # String containing details of the breach, used to check if this is a new breach
                breachInfo = ','.join([emailAddress, breachTitle, breachDate, breachModified])

                # Checks if this breach has been previously detected
                with open('KnownBreaches.csv','r') as knownBreaches:

                    # Breaches are determined to be new unless they are found in KnownBreaches.csv
                    newBreach = True

                    # Amendments are determined to be unnecessary unless an updated date is found
                    amendBreach = False
                    breachToAmend = None

                    # Cycling through every known breach in KnownBreaches.txt
                    for pastBreach in knownBreaches.read().splitlines():
                        pastBreachSplit = pastBreach.split(',')

                        # If this breach is already known to have happened
                        if pastBreachSplit[0] == emailAddress and pastBreachSplit[1] == breachTitle and pastBreachSplit[2] == breachDate:

                            newBreach = False

                            # If this breach has not been updated
                            if pastBreachSplit[3] == breachModified:
                                breachLogger.debug('The ' + breachTitle + ' breach on ' + breachDate + ' is already in the list of known breaches.')

                            # If this breach has been updated since the last run
                            else:
                                breachLogger.info('There has been an update to the ' + breachTitle + ' breach on ' + breachDate + ' since the last check!')
                                amendBreach = True
                                breachToAmend = pastBreach

                            # If a matching breach has been found, break the loop
                            break

                # This breach is not in the list of known breaches
                if newBreach == True:
                    breachLogger.debug(breachTitle + ' is not in the list of known breaches.')
                    newBreachCount += 1
                    newBreachesTotal += 1

                    # Add this breach to the file
                    with open('KnownBreaches.csv','a') as knownBreaches:
                        knownBreaches.write(breachInfo + '\n')
                        breachLogger.debug('Writing ' + breachTitle + ' to the list of known breaches.')

                        # Presentation function only
                        if newBreachCount == 1:
                            breachLogger.warning('New breach(es) for ' + emailAddress + ' have been logged! ')

                        # Gives the user details of the breach
                        breachLogger.warning(' '*10 + breachTitle + ' was breached on ' + breachDate + '!')

                # If this breach is in the list of known breaches, but needs to be updated
                elif amendBreach == True:

                    amendedBreachesTotal += 1

                    with open('KnownBReaches.csv') as knownBreachesAll:
                        knownBreaches = knownBreachesAll.read().splitlines()

                    with open('KnownBreaches.csv', 'w') as knownBreachesAmend:
                        for knownBreach in knownBreaches:
                            if knownBreach == breachToAmend:
                                knownBreachesAmend.write(breachInfo + '\n')
                            else:
                                knownBreachesAmend.write(knownBreach + '\n')

            breachLogger.debug('newBreachCount = '  + str(newBreachCount))

            # If there are no new breaches, tell the user
            if newBreachCount == 0:
                breachLogger.info('The email address ' + emailAddress + ' has not been breached since the last check!')

        # A 404 response indicates the account has not been breached
        elif checkEmail.status_code == 404:
            breachLogger.info('The email address ' + emailAddress + ' has not been breached since the last check!')

        # If an unknown response was received from the API
        else:
            breachLogger.error('Unable to check ' + emailAddress +
                            ', received a ' + str(checkEmail.status_code) +
                            ' ' + str(checkEmail.reason) +
                            ' response from the HaveIBeenPwned API!')
            breachLogger.debug(checkEmail.content)

        # Add in a delay to limit the rate of requests (as per API spec)
        sleepTime = 2
        breachLogger.debug('Sleeping for ' + str(sleepTime) + ' seconds.')
        sleep(sleepTime)

breachLogger.info('Checking run finished - {} new breaches detected,'\
                  ' {} breaches have updated information.'.format(newBreachesTotal,amendedBreachesTotal))
