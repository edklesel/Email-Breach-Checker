"""
Author - Edward Klesel

"""


import requests
import json
import os
import logging
from time import sleep

hackLogger = logging.getLogger('HackLogger')
hackLogger.setLevel(logging.DEBUG)

logFile = logging.FileHandler('EmailBreachCheck.log')
# logFormat = "%(asctime)s - %(levelname)s - %(message)s"
logFormatter = logging.Formatter("%(levelname)-8s - %(asctime)s.%(msecs)03d - %(message)s", '%Y-%m-%d %H:%M:%S')
logFile.setFormatter(logFormatter)
logFile.setLevel(logging.DEBUG)
hackLogger.addHandler(logFile)

hackLogger.info('-----------------------------------')
hackLogger.info('Beginning checking Run:')

newHacksTotal = 0

try:
    # Read email accounts from txt file
    with open('accounts.txt', 'r') as t:

        # Read each email address
        for line in t.read().splitlines():
            # Make the GET request
            checkEmail = requests.get('https://haveibeenpwned.com/api/v2/breachedaccount/' + line)
            # print('')
            # print('Checking ' + line + ' to see if it has been hacked...')
            hackLogger.info('Checking ' + line + ' to see if it has been hacked...')

            newHackCount = 0

            # A 200 OK response indicates that the account has been hacked

            hackLogger.debug('Response code = ' + str(checkEmail.status_code) + ' ' + str(checkEmail.reason))

            if checkEmail.status_code == 200:

                # Loads the response from the HaveIBeenPwned API
                hackDetails = json.loads(checkEmail.content)

                # Loops through each hacked site
                for hack in hackDetails:

                    hacksToLog = []

                    # Creates a file containing previous hacks, if one doesnt exist
                    if not os.path.isfile('KnownHacks.csv'):
                        with open('KnownHacks.csv','w') as KnownHacks:
                            KnownHacks.write('email,title,breachdate,modifieddate')
                            hackLogger.debug('No known hacks found. Creating list of known hacks.')

                    # Entry to write into file of previous hacks, used to check if a new hack has been found
                    logHack = line + ',' + hack['Title'] + ',' + hack['BreachDate'] + ',' + hack['ModifiedDate']

                    # Checks if this hack has been previously detected
                    with open('KnownHacks.csv','r') as hacks:
                        if logHack not in hacks.read().splitlines():
                            hacksToLog.append(logHack)
                            newHackCount += 1
                            newHacksTotal += 1

                    # Gives the user details of the new hack
                    if newHackCount > 0:
                        if newHackCount == 1:
                            hackLogger.warning('New hack(s) for ' +
                                  line +
                                  ' have been logged! ')

                        hackLogger.warning(
                              ' '*10 +
                              hack['Title'] +
                              ' was breached on ' +
                              hack['BreachDate'] +
                              '!')

                    # If there are new hacks, add them to the file
                    if hacksToLog != []:
                        with open('KnownHacks.csv','a') as hacks:
                            for writeHack in hacksToLog:
                                hacks.write(writeHack + '\n')

                # If there are no new hacks, tell the user
                hackLogger.debug('newHackCount = '  + str(newHackCount))
                if newHackCount == 0:
                    # No new breaches have been registered.
                    hackLogger.info('The email address ' + line + ' has not been hacked since the last check!')

            # A 404 response indicates the account has not been hacked
            elif checkEmail.status_code == 404:
                # print('The email address ' + line + ' has not been hacked since the last check!')
                hackLogger.info('The email address ' + line + ' has not been hacked since the last check!')

            else:
                hackLogger.error('Unable to check ' + line +
                                ', received a ' + str(checkEmail.status_code) +
                                ' ' + str(checkEmail.reason) +
                                ' response from the HaveIBeenPwned API!')
                hackLogger.debug(checkEmail.content)

            # Add in a delay to limit the rate of requests (as per API spec)
            sleepTime = 2
            hackLogger.debug('Sleeping for ' + str(sleepTime) + ' seconds.')
            sleep(sleepTime)

except:
    hackLogger.warning('No accounts.txt found.')
hackLogger.info('Checking run finished - {} new hacks detected.'.format(newHacksTotal))