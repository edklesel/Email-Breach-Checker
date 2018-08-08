#Accounts
- Multiple accounts can be stored in this section, in array format.

###Address
- String
- A simple email address of the form "test@email.com"

###Breach Alert
- Boolean (1 or 0)
- Tells the program if the owner of the address wants to receive email notifications on the detection of a new alert.

###Monthly Stats
- Boolean (1 or 0)
- Tells the program if the user would like to receive monthly stats on the breaches in the last month.

#Alerting

###Server
- String
- The address of the SMTP server used to send emails, e.g "smtp.gmail.com"

###Port
- Integer
- Port number used to connect to the SMTP server, e.g 587

###Address
- String
- Email address of the email that breach alert emails are to be sent from.

###Password
- String
- Password to the above email address

###Signature
- String
- Name with which to sign off alerting emails.

#Run

###Sleep Time
- Integer
- The time which to sleep in-between API requests.
- This is recommended to be 2 seconds or longer, as per API spec.

###Known Breaches
- String
- File path at which to write and read the .csv file containing known breaches.

#User Agent

###User-Agent
- String
- A header used in the API request, allowing the API to identify who is making the request.

###From
- String
- Email address of the person (you) who is making the request.

#Logging

###Location
- String
- Location at which to store logs

###Format
- String
- Format used for the logging (see python logging module for details), e.g "%(levelname)-7s - %(asctime)s.%(msecs)03d - %(message)s"

###Date Format
- String
- Format for the date used in log entires, e.g "%Y-%m-%d %H:%M:%S"