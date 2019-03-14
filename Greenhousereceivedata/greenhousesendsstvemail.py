#!/usr/bin/python3.5
# encoding: utf-8

# greenhousesendsstvemail.py
# Copyright (C) 2019 The Groundhog Whisperer
#
# Requirements: 
# QSSTV - Qt based slow scan television and fax
# Python 3
#
# Produces:
# Email messages containing SSTV image data received via a radio tranmissions
#
# This script monitors a folder for .png image files produced by QSSTV
# transmissions generated by greenhousestatusttsrttysstvrf.py
# This script locates the most recently created image file in the
# folder and sends the image as an email message attachment.
# The most recent image file name sent via email is recorded for future
# comparison to prevent retranmission of the same SSTV image file.

# Executed using crontab -e
# */5 * * * * /usr/bin/python3 /home/livestream/greenhousesendsstvemail.py

import time
from smtplib import SMTP
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.headerregistry import Address
from ssl import SSLContext, PROTOCOL_TLSv1_2
import glob
import os


def send_sstv_email_message():
    
    # Return a list of path names for the folder containing the QSSTV image files
    list_of_files = glob.glob('/home/livestream/*.png') 
    # Return the latest image file found in the folder
    latest_file = max(list_of_files, key=os.path.getctime)

    # Define the path and name of the text file storing the name of the last image file sent
    last_image_name_list_file = '/home/livestream/lastimg.txt'
    # Open the file for reading
    last_image_name_list = open(last_image_name_list_file,'r')
    # Read the value of the last image file sent
    latest_image_name_sent = last_image_name_list.read()
    # Close the file
    last_image_name_list.close()

    print('Youngist SSTV image file: ')
    print(latest_file)
    print('Last SSTV image file sent: ')
    print(latest_image_name_sent)

    # Compare the last record file name to the most recent file found in the folder to determine if we send email
    if (latest_file != latest_image_name_sent):
        print('We send now and record the file name.')
        # Open the text file storing the name of the last image sent for writing
        last_image_name_list = open(last_image_name_list_file,'w')
        # Update the value stored in the text file with the new file name value we are sending now
        last_image_name_list.write(latest_file)
        # Close the file
        last_image_name_list.close()

        # Creating an email object
        msg = EmailMessage()
        # Set the sender address
        msg['From'] = 'somefromaddress@email.example'
        # Set the destination addresses
        recipients = ['sometoaddress@email.example', 'sometoaddress@email.example']
        # Join the recipients addresses into one string and set the destination values
        msg['To'] = ", ".join(recipients)
        # Set the message subject
        msg['Subject'] = 'SSTV/SMS courtesy Ay-yah\'s Horticultural Automation Systems'    

        # Open the SSTV image file for reading in binary mode
        fp = open(latest_file, 'rb')
        # MIME encode image
        att = MIMEImage(fp.read())
        # Close the image file
        fp.close()

        # Define the file name and prefix the file with our local second since Unix epoch time stamp
        file_name = '%s_SSTV_Image.png' % time.time()
        # Define the filename of the attached file
        att.add_header('Content-Disposition', 'attachment', filename='%s' % file_name)
        # Convert the message to multipart/mixed content
        msg.make_mixed()
        # Add the attachment to the multipart message content
        msg.attach(att)

        # Define the SMTP server connection
        with SMTP(host=''smtp.email.example', port=587) as smtp_server:
            try:
                # Establish a secure SSL connection to the SMTP server
                smtp_server.starttls(context=SSLContext(PROTOCOL_TLSv1_2))
                # Provide authentication credentials
                smtp_server.login(user='somefromaddress@email.example', password='shhhhapasswordvalue')
                # Send the email message
                smtp_server.send_message(msg)

            except Exception as e:                
                print('Error sending email. Details: {} - {}'.format(e.__class__, e))

send_sstv_email_message()