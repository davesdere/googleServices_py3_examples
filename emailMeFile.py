# David Cote 2018
# https://docs.python.org/3/library/email.examples.html
#!/usr/bin/env python
# encoding: utf-8
# Python 3
# Works on Raspbian Jessie

# To check if file exists
from os.path import isfile
import datetime
import csv
import requests
from bs4 import BeautifulSoup
import sys

# Allow script to understand argument. You can just add the filename of the file
# you want to send. It has to be in the same folder. 
if len(sys.argv) < 2:
    # The name of the file to send
    print("Sending a file by email")
    filename = input("What is the filename? ")
if len(sys.argv) == 2:
    filename = sys.argv[1]
#if not os.path.exists(sys.argv[1]):
#    sys.exit('ERROR: File %s was not found!' % sys.argv[1])

# Increment a date variable
now = datetime.datetime.now()
filedate = str(now.day)
filedate += "_"
filedate += str(now.month)
filedate += "_"
filedate += str(now.year)


# To send an email
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '

def main(filename):
    sender = 'emailFrom@gmail.com'
    gmail_password = 'password'
    # You can have more than one separated by a comma within quotes
    recipients = ['emailTo@anyemail.com']
    
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'Sent with Python3 -> '+filename
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'This might be hidden.\n'

    # List of attachments
    attachments = []
    attachments.append(filename)

    # Add the attachments to the message
    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)
        except:
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            raise

    composed = outer.as_string()

    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
        print("Email sent!")
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise

if __name__ == '__main__':
    # Check if file exists
    print("q to cancel")
    # Because sometimes I like to joke
    god = True
    while god:
        if isfile(filename):
            print("File ", filename, " found.")
            main(filename)
            god = False
        else:
            if filename == "q":
                print("Cancelled")
                god = False
                break
            print("The file doesn't seem to exist")
            filename = input("What is the filename? ")
    
