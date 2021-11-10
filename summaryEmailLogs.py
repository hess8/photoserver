
from datetime import datetime, timedelta, date
import sys, os, shutil
import ssl, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# import pytz
# from time import sleep
# from numpy import bool_, float32, mod, round, sort, unicode_, zeros
# from funcs import boolFromStr,checkOutofState, getOLCFlightIDs, localFromUTC, publish, rank, readfile, readMembers,\
#     requestWait, save, time_until_end_of_day, writeFile
sys.path.append('/home/bret/secure')
from photoserverEmail import *  #ignore the red lines...it reads these
from funcs import readfile, writeFile
basepath = os.path.curdir
logsPath = '{}/logs'.format(basepath)
if not os.path.exists(logsPath):
    os.mkdir(logsPath)
timestamp = datetime.now().replace(microsecond=0).isoformat()
latestLog = '{}/rsync.log'.format(logsPath)
logFile = '{}/rsync{}.log'.format(logsPath,timestamp)
summaryFile = '{}/summary{}.log'.format(logsPath,timestamp)
# print(os.path.getctime(latestLog))
lines = readfile(latestLog)
summary = []
summaryStr=''
newData = False
keepTags = [' >f', ' sent ', 'total size']
for line in lines:
    if ' >f' in line:
        newData = True
        break
#Make summary and email
if newData:
    for line in lines:
        for tag in keepTags:
            if tag in line:
                summary.append(line)
                summaryStr += line + '<br>\n'
                # print (line)
                break
    subject = 'Photoserver rsync summary {}'.format(timestamp)
    html = '<!DOCTYPE html>\n'
    html += '<html>\n'
    html += '<head>\n'
    html += '<style> body {font-family:courier, courier new, serif;} </style>\n'
    html += '<body>\n'
    html += '<p>\n'
    html += summaryStr
    html += '</p>\n'
    html += '</body>\n'
    html += '</head>\n'
    html += '</html>\n'

    # body = '<font="Font Name Here">Your e-mail here</font>summaryStr
    body = html
    print (body)
    writeFile(summaryFile, summary)
else:
    print ('No files transferred')
    subject = 'No photoserver file changes'
    body = 'Executed summaryEmailLogs'

context = ssl.create_default_context()
# try:
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(email_from, email_pw)
    print ('Email login successful')
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = email_from
    message["To"] = email_to
    # message.attach(MIMEText(body, "plain"))
    message.attach(MIMEText(body, "html"))
    server.sendmail(
        email_from, email_to, message.as_string())
# except:
#     print("Can't connect to email server or send email.  Reading login info from ../secure/photoserverEmail.py")
writeFile(logFile,lines)
# print (summaryStr)
print ('Done')