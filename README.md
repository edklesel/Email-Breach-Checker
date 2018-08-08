# Email-Breach-Checker
Daily process which makes requests to the HaveIBeenPwned API to check for email account breaches, and will email the user if a breach has been detected.

--------

## To use:
- Create an email account (preferably gmail) to use to send emails from, which you will receive if a breach has been detected. See sendEmail.py for details.
- Add email accounts to Config.json which you want to be checked for breaches.
- Add remaining information to config (see Config.json.md for details)
- Run main.py to request information on said accounts from HaveIBeenPwned.com's database
