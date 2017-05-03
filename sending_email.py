import os
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
import smtplib
from email import Encoders
import time


def send_email(subject, body, attachement=None):
    with open('credentials.txt') as f:
        credentials = [x.strip().split(':') for x in f.readlines()]

    gmail_user = credentials[0][1]
    gmail_pwd = credentials[0][2]
    recipient = credentials[1][1]

    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = COMMASPACE.join(recipient)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    msg.attach( MIMEText(body) )

    if not attachement is None:
        part = MIMEBase('application', "octet-stream")
        part.set_payload( open(attachement,"rb").read() )
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment; filename="%s"'
                       % os.path.basename(attachement))
        msg.attach(part)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo_or_helo_if_needed()
        server.starttls()
        server.ehlo_or_helo_if_needed()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(gmail_user, recipient, msg.as_string())
        server.close()
        print 'successfully sent the mail'
    except Exception as e:
        print e
        print "failed to send mail"


def send_error_mail(e):
    subject = "Error!"
    body = time.strftime("%Y_%m_%d_%H_%M_%S") + "\n" + str(e)
    send_email(subject, body)


def send_end_of_errors_mail(error_counter):
    subject = "End of errors!"
    body = time.strftime("%Y_%m_%d_%H_%M_%S") + "\n" + "Errors stopped after " + str(error_counter)
    send_email(subject, body)


def send_data(date):
    subject = "Data from: " + date
    body = ""
    attachement = date+".zip"
    send_email(subject, body, attachement=attachement)
