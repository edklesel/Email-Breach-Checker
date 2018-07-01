import requests
import json
import os
import logging
from time import sleep

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

# Creates a file containing previous breaches, if one doesnt exist
if not os.path.isfile('KnownBreaches.csv'):
    with open('KnownBreaches.csv', 'w') as knownBreaches:
        knownBreaches.write('email,title,breachdate,modifieddate\n')
        breachLogger.debug('No known breaches found. Creating list of known breaches.')

# Read email accounts from txt file
with open('accounts.txt', 'r') as t:

    # Read each email address
    for line in t.read().splitlines():

        # Make the GET request
        checkEmail = requests.get('https://haveibeenpwned.com/api/v2/breachedaccount/' + line)
        breachLogger.info('Checking ' + line + ' to see if it has been breached...')

        newBreachCount = 0

        breachLogger.debug('Response code = ' + str(checkEmail.status_code) + ' ' + str(checkEmail.reason))

        # A 200 OK response indicates that the account has been breached
        if checkEmail.status_code == 200:

            # Loads the response from the HaveIBeenPwned API
            breachDetails = json.loads(checkEmail.content)


            # Loops through each breached site
            for breach in breachDetails:


                # Entry to write into file of previous breaches, used to check if a new breach has been found
                breachInfo = line + ',' + breach['Title'] + ',' + breach['BreachDate'] + ',' + breach['ModifiedDate']

                # Checks if this breach has been previously detected
                with open('KnownBreaches.csv','r') as knownBreaches:
                    if breachInfo not in knownBreaches.read().splitlines():
                        breachLogger.debug(breach['Title'] + ' is not in the list of known breaches.')
                        newBreachCount += 1
                        newBreachesTotal += 1
                        logBreach = True
                    else:
                        breachLogger.debug('The ' + breach['Title'] + ' on ' + breach['BreachDate'] + ' is already in the list of known breaches.')
                        logBreach = False

                # Gives the user details of the new breach
                if newBreachCount > 0:
                    if newBreachCount == 1:
                        breachLogger.warning('New breach(es) for ' + line + ' have been logged! ')

                    breachLogger.warning(' '*10 + breach['Title'] + ' was breached on ' + breach['BreachDate'] + '!')

                # If this is a new breach, add it to the file.
                if logBreach == True:
                    with open('KnownBreaches.csv','a') as knownBreaches:
                        knownBreaches.write(breachInfo + '\n')
                        breachLogger.debug('Writing ' + breach['Title'] + ' to the list of known breaches.')

            breachLogger.debug('newBreachCount = '  + str(newBreachCount))

            # If there are no new breaches, tell the user
            if newBreachCount == 0:
                breachLogger.info('The email address ' + line + ' has not been breached since the last check!')

        # A 404 response indicates the account has not been breached
        elif checkEmail.status_code == 404:
            breachLogger.info('The email address ' + line + ' has not been breached since the last check!')

        # If an unknown response was received from the API
        else:
            breachLogger.error('Unable to check ' + line +
                            ', received a ' + str(checkEmail.status_code) +
                            ' ' + str(checkEmail.reason) +
                            ' response from the HaveIBeenPwned API!')
            breachLogger.debug(checkEmail.content)

        # Add in a delay to limit the rate of requests (as per API spec)
        sleepTime = 2
        breachLogger.debug('Sleeping for ' + str(sleepTime) + ' seconds.')
        sleep(sleepTime)

breachLogger.info('Checking run finished - {} new breaches detected.'.format(newBreachesTotal))