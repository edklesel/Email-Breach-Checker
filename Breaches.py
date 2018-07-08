"""

Title:  Breaches
Author: Edward Klesel
Date:   08/07/2018

Description:    Defines classes used in the breachHistory module, to define Breaches and Past Breaches.

Classes:

Breach -        Breach containing data from the HaveIBeenPwned API, which allows main() to determine whether to
                write this breach to file, amend this breach of do nothing at all.

PastBreach -    Breach containing data form the file listing known breaches, which is used to determine whether
                the breach defined in Breach is new or whether it has been seen before.

"""



from iso8601 import parse_date

class Breach:

    def __init__(self, Address, breachDetails):

        self.Address = Address
        self.Title = breachDetails['Title']
        self.BreachDate = breachDetails['BreachDate']
        self.ModifiedDate = str(parse_date(breachDetails['ModifiedDate']).date())
        self.Info = ','.join([self.Address,self.Title,self.BreachDate,self.ModifiedDate])
        self.CoreInfo = [self.Address,self.Title,self.BreachDate]
        self.Write = None
        self.Amend = None


class PastBreach:

    def __init__(self, breachInfo):

        self.Address =  breachInfo.split(',')[0]
        self.Title = breachInfo.split(',')[1]
        self.BreachDate = breachInfo.split(',')[2]
        self.ModifiedDate = breachInfo.split(',')[3]
        self.CoreInfo = [self.Address,self.Title,self.BreachDate]