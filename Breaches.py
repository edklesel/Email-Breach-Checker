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