import datetime
import threading
import sys
import smtplib

gmailAddress = 'ENTER YOUR EMAIL ADDRESS HERE'
password = 'ENTER YOUR PASSWORD HERE'
#Enable less secure apps in gmail - https://support.google.com/accounts/answer/6010255?hl=en


def log(txt):
	logFile = 'PythonMailer.log'
	logMsg = '\n'+str(datetime.datetime.now())+'    ' + str(txt)
	with open(logFile,'a') as f:
		f.write(logMsg)
        
def mailer(recipient, subject, body):
    try:
        subject = 'RPi3 - mainsChecker : '+subject
        thredMail = threading.Thread(target=mailerActual,args=(recipient,subject,body,))
        thredMail.start()
    except Exception as e:
        msg = 'send mail failed : '+str(e)
        lineNoMailException =sys.exc_info()[-1].tb_lineno
        print(msg)
        print(lineNoMailException)
        log(msg)
        log(lineNoMailException)

def mailerActual(recipient, subject, body):
    pwd = password
    FROM = gmailAddress
    user = FROM
    TO = recipient if isinstance(recipient, list) else [recipient]
    SUBJECT = subject + " " + str(datetime.date.today())
    TEXT = body

    # Prepare actual message
    message = """From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(user, pwd)
        server.sendmail(FROM, TO, message)
        server.close()
        msg = "Mail with subject '" + SUBJECT + "' sent Succesfully to "+ recipient
        print(msg)
        log(msg)
    except Exception as e:
        msg = 'Exception : '+str(e)
        lineNoMailException =sys.exc_info()[-1].tb_lineno
        print(lineNoMailException)
        print(msg)
        log(lineNoMailException)
        log(msg)
        
