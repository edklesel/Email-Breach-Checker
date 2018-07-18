"""

Title:  classes
Author: Edward Klesel
Date:   09/07/2018

Description -

Classes:

Run -       Run is a class to contain the information about the current checking run,
            containing attributes used to tell the user how many new/amended breaches
            have been found during this checking run.

Address -   Address is a class detailing the email address, which contains information
            about the number of breaches associated with that email address.

"""

import datetime

class Run:

    def __init__(self):

        self.newBreaches = 0
        self.amendedBreaches = 0
        self.date = datetime.datetime.now().date()
        self.time = datetime.datetime.now().time()
