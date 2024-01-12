#!/usr/bin/python3
#Written by wai.phyo6
import os
import sys
import subprocess
import smtplib
import base64
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

sender = 'notify2@frontiir.net'
#recipient = 'sysops@frontiir.net'
#recipient = 'lwin.moeaung2@frontiir.net'

recipient = 'wai.phyo6@frontiir.net'
def send_mail():
	try:
		sender = 'notify2@frontiir.net'
		SMTP_SERVER = 'zcs.frontiir.net'
		SMTP_PORT = 587
		session = smtplib.SMTP('zcs.frontiir.net', 587)
		session.ehlo()
		session.starttls()
		session.ehlo
		session.login(sender, 'sdfljlERsdf34#')
		session.sendmail(sender, recipient, msg.as_string())
		session.quit()
		print("Mail Sent Successfully")
	except Exception:
		print("Error: unable to sent")

path_to_file = 'result.txt'
path = Path(path_to_file)

if path.is_file():
	frrconfig = subprocess.run(['cat','%s' % '/root/object_storage_report/result.txt'], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL).stdout.decode('utf-8')
#	print ("file exist")

	msg = MIMEText(frrconfig)

	msg['From'] = 'Notify <notify2@frontiir.net>'
	msg['To'] = recipient
	msg['Subject'] = '[Alert] Object Storage Size Check'

	if __name__=='__main__':
		send_mail()

else: 
	frrconfig = "Plase check your health check data files and database cluster."
	msg = MIMEText(frrconfig)
	msg['From'] = 'Notify <notify2@frontiir.net>'
	msg['To'] = recipient
	msg['Subject'] = 'File Error : Result File Does not Exists'

	if __name__=='__main__':
		send_mail()
