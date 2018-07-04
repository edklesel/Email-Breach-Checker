# Email-Breach-Checker
Daily process which makes requests to the HaveIBeenPwned API to check for email account breaches

--------

## To use:
- Edit accounts.txt to include all email accounts you wish to check for breaches.
- Run main.py to request information on said accounts from HaveIBeenPwned.com's database



## To do:
- ~~Create a seperate debug and info/warning log file~~  01/07/2018
- ~~Edit variable names, chanigng "hack" to something less silly~~ 01/07/2018
- ~~Change the "Modified Date" date format to either just a date or a datetime~~ 04/07/2018
- If a breach has been previously detected, check if the modified date is different. If so, let the user know there's been an update.
