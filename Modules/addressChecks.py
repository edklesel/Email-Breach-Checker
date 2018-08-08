"""

Title:  AddressChecks
Author: Edward Klesel
Date:   05/07/2018

Description:    This module contains methods used in EmailBreachChecker to validate
                email addresses, and to check them by making requests to the
                HaveIBeenPwned API.

"""


import json
import requests
from time import sleep
import re
from Modules.breachLogging import breachLog
from Modules import breachHistory
from Modules.sendEmail import sendEmail

# Load config
with open('Config.json', 'r') as f:
    config = json.loads(f.read())
sleepTime = config['Run']['Sleep Time']
headers = config['User Agent']


def checkAddress(account, run):

    """

    Title:  checkAddress
    Author: Edward Klesel
    Date: 05/08/2018

    Description: Check an email address against the HaveIBeenPwned API.


    Arguments:

        account     A dictionary containing an email address, and booleans
                    to determine whether or not to send emails and to send
                    monthly stats.

        run         An object containing information about the current
                    checking run, such as number of breaches, amendments and
                    date/times.

    """

    emailAddress = account['Address']

    # Test the connection to the API
    try:
        breachLog('info', 'Checking ' + emailAddress + ' to see if it has been breached...')
        testRequest = requests.get('https://haveibeenpwned.com/api/v2/breachedaccount/test@example.com',
                                   headers=headers)
        breachLog('debug',
                  'Connection to the HaveIBeenPwned API established. Response code: {}'.format(testRequest.status_code))

        # Add in a delay to limit the rate of requests (as per API spec)
        breachLog('debug', 'Sleeping for ' + str(sleepTime) + ' seconds.')
        sleep(sleepTime)

    # If no connection can be made, catch the error
    except requests.exceptions.ConnectionError as e:
        breachLog('error', 'Unable to connect to the HaveIBeenPwned API.')
        breachLog('error', e)
        return

    # Make the GET request
    URL = 'https://haveibeenpwned.com/api/v2/breachedaccount/' + emailAddress
    checkEmail = requests.get(URL, headers=headers)

    newBreachCount = 0

    breachLog('debug', 'Making request to {} .'.format(URL))
    breachLog('debug', 'Response code = ' + str(checkEmail.status_code) + ' ' + str(checkEmail.reason))

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

                if account['Breach Alert'] == 1:
                    sendEmail(newBreach)

                # Presentation function only
                if newBreachCount == 1:
                    breachLog('warning', 'New breach(es) for ' + emailAddress + ' have been logged! ')

                # Gives the user details of the breach
                breachLog('warning', ' ' * 10 + newBreach.Title + ' was breached on '
                                     + newBreach.BreachDate + '!')

            # If this breach is in the list of known breaches, but needs to be updated
            elif newBreach.Amend is True:

                run.amendedBreaches += 1
                breachHistory.amendBreach(newBreach)
                breachLog('debug', 'newBreachCount = ' + str(newBreachCount))

        # If there are no new breaches, tell the user
        if newBreachCount == 0:
            breachLog('info', 'The email address ' + emailAddress +
                              ' has not been breached since the last check!')

    # A 404 response indicates the account has not been breached
    elif checkEmail.status_code == 404:
        breachLog('info', 'The email address ' + emailAddress + ' has not been breached since the last check!')

    # If an unknown response was received from the API
    else:
        breachLog('error', 'Unable to check ' + emailAddress + ', received a ' + str(checkEmail.status_code) +
                           ' ' + str(checkEmail.reason) + ' response from the HaveIBeenPwned API!')
        breachLog('debug', checkEmail.content)


def validateAddress(address):

    """

    Title:  validateAddress
    Author: Edward Klesel
    Date:   07/08/2018

    Description:    Simple regex function used to determine whether or not an email address
                    follows the basic address structure.


    Arguments:

        address     A simple string containing an email address.


    Returns:

        True        If the email address is of the correct structure.

        False       Otherwise.

    """


    # This searches for emails following the format username@hostname.topleveldomain e.g test@example.com
    reFormat = r'[a-zA-Z0-9.]+\@[a-zA-Z0-9]+\.[a-zA-Z]+'
    match = re.search(reFormat, address)

    if match:
        return True
    else:
        return False
