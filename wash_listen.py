import serial                                       #serial library
import re                                           #string manipulation library
import smtplib, ssl                                 #email libraries
import numpy as np

ser = serial.Serial('/dev/ttyUSB0',9600)           #usb serial for arduino

encoding = 'utf-8'                                  #decode from b-string

washerOn = 0                                        #state of washer
stdDev = 0
counter = 0
array = [505,505,505,505,505,505,505,505,505,505]
port = 587                                          # local email client port
smtp_server = "smtp.gmail.com"                      #gmails email server
sender_email = "letsdoitlivebots@gmail.com"         #my dedicated robot email
receiver_email = "anonymousquantumstudent@gmail.com"    #personal email
password = "letsdoitlive"                           #robot email password
messageStart = """\                                
Subject: washer started

I heard a noise"""

messageEnd = """\
Subject: washer ended

no more noise"""





context = ssl.create_default_context()
while True:                                         #always listen to mic
    line = ser.readline()                           #read arduino/mic
    string = line.decode(encoding)                  #convert to string
    array[counter] = float(string)                  #load this noise into the array
    counter += 1    #get ready for next noise
    counter = counter%10                            #make sure we dont leave the array
    stdDev = np.std(array)                          #get the standard deviation of the noise
    if(stdDev > 5 and washerOn == 0):               #someone started the washer
        washerOn = 1 #make sure system knows that
        print("washer on, sending email")
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, messageStart)
    if(stdDev < 5 and washerOn == 1):       #washer stopped
        washerOn = 0     #record washer stopping
        print("washer off, sending email")
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, messageEnd)