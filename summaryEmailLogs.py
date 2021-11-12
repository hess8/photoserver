
from datetime import datetime, timedelta, date
import sys, os, shutil
import ssl, smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


sys.path.append('/home/bret/secure')
from photoserverEmail import *  #ignore the red lines...it reads these
from funcs import diskUsage, readfile, writeFile

os.chdir('/home/bret/photoserver/')
basepath = os.path.curdir
logsPath = 'logs/'
if not os.path.exists(logsPath): os.mkdir(logsPath)
backupDir = '/media/sf_backup/photoserverLychee/rsyncLychee'
lines = readfile('lastBackupSize.txt')
lastBackupSize = None
backupIncr = None
if len(lines) > 0:
    lastBackupSize = int(readfile('lastBackupSize.txt')[0])
totalBackupSize = int(diskUsage(backupDir)) # Mb
timestamp = datetime.now().replace(microsecond=0).isoformat()
latestLog = 'logs/rsync.log'
logFile = 'logs/rsync{}.log'.format(timestamp)
summaryFile = 'logs/summary{}.log'.format(timestamp)
# print(os.path.getctime(latestLog))
lines = readfile(latestLog)
if len(lines) == 0: sys.exit('Stop.  logs/rsync.logs is empty or does not exist')
summary = []
summaryStr=''
newData = False
keepTags = [' >f', ' sent ', 'total size']
for line in lines:
    if ' >f' in line and '/.git/objects/pack/pack' not in line:
        newData = True
        break
for line in lines:
    for tag in keepTags:
        if tag in line:
            summary.append(line)
            summaryStr += line + '<br>\n'
            break
writeFile(logFile,lines)
print (summaryStr)

for line in summary:
    if 'total size' in line:
        rsyncTot = int(int(line.replace(',','').split('is')[1].split('speedup')[0])/1e6)
          #Mb
    elif ' sent ' in line:
        rsyncRec = int(int(line.replace(',','').split('received')[1].split('bytes')[0])/1e6) #Mb
if lastBackupSize:
    backupIncr = totalBackupSize - lastBackupSize #read from disk
    print('Stored increment', backupIncr)
else:
    print('lastBackupSize could not be read')
print('rsyncTot', rsyncTot)
print ('totalBackupSize',totalBackupSize)
print ('rsyncRec', rsyncRec)


writeFile('lastBackupSize.txt',[str(totalBackupSize)])
alerts = []

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
html

#Make summary and email
if backupIncr is not None and backupIncr < 0:
    print ('Backup size has decreased!')
    subject = 'Photoserver backup size has decreased!'
    body = html
    writeFile(summaryFile, summary)
elif newData:
    subject = 'Photoserver rsync summary {}'.format(timestamp)
    body = html
    writeFile(summaryFile, summary)
else:
    print ('No files transferred')
    subject = 'No photoserver file changes'
    body = 'Executed summaryEmailLogs'

context = ssl.create_default_context()
try:
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
except:
    print("Can't connect to email server or send email.  Reading login info from ../secure/photoserverEmail.py")

print ('Done')