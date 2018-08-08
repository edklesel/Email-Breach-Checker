"""

Title:  cRun
Author: Edward Klesel
Date:   09/07/2018

Description -   Module containing classes used during a checking run.

"""

import datetime


class Run:

    """

    Title:  Run
    Author: Edward Klesel
    Date:   09/07/2018

    Description:    Run is a class to contain the information about the current checking run,
                    containing attributes used to tell the user how many new/amended breaches
                    have been found during this checking run, as well as the date/time the
                    run began.

    """

    def __init__(self):

        self.newBreaches = 0
        self.amendedBreaches = 0
        self.date = datetime.datetime.now().date()
        self.time = datetime.datetime.now().time()
