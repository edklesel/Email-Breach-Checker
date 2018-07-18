"""

Title: sendEmail
Author: Edward Klesel
Date: 15/07/2018

Description:    sendEmail is a module which uses a gmail SMTP server to send an email
                to an address which has had an account breached. If a new breach is
                detected, an email is sent to the relative address giving the user details
                of the breach.

"""

import smtplib
from email.mime.text import MIMEText
from breachLogging import breachLog

# Your name
name = 'Edward Klesel'

def sendEmail(breach):

    # Email account used to send email addresses
    # You will need to create your own "email" and "password"
    # files containing the email address you want to send emails from
    sendAddress = open('email','r').read()
    sendPassword = open('password','r').read()

    # Build the SMTP server connection
    smtpServer = 'smtp.gmail.com'
    port = 587
    server = smtplib.SMTP()
    breachLog('debug','Connecting to the SMTP server @ ' + smtpServer + ':' + str(port))
    server.connect(smtpServer, port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    breachLog('debug','Connection to the SMTP server established.')
    breachLog('debug','Logging in to the SMTP server as ' + sendAddress + '.')
    server.login(sendAddress, sendPassword)
    breachLog('debug','Logged in successfully.')

    # Construct the message to be sent
    messageRaw = "<html>\n"\
    + "<head></head>\n"\
    + "<body>"\
    + "<p>Attention user!</p>\n\n"\
    + "<p>A breach has been detected for your account, {0}, on the website {1}. This account was breached on {2}.</p>\n\n"\
    + "<p>{3}</p>\n\n"\
    + "<p>It would be advised that you change your password on this website, to protect your information.<p>\n\n"\
    + "<p> This was an automated message.</p>\n"\
    + "<p> If you have any queries about this message, contact {}.</p>\n".format(name)\
    + "</body>\n"\
    + "</html>"

    message = messageRaw.format(breach.Address, breach.Site, breach.BreachDate, breach.Body).encode('utf-8')

    msg = MIMEText(message, 'html','UTF-8')

    msg['Subject'] = 'New breach detected for {}'.format(breach.Address)
    msg['From'] = sendAddress
    msg['To'] = breach.Address

    # Send the message
    try:
        breachLog('debug', 'Sending email to {} to warn them of the breach!'.format(breach.Address))
        server.send_message(msg=msg)
        breachLog('debug','Email sent.')
    except Exception as e:
        breachLog('error', 'Unable to send email to {}, see debug log for details.'.format(breach.Address))
        breachLog('debug', e)

    # Close the SMTP connection
    server.quit()
