# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 14:14:06 2021

@author: Thennan
gpiozero uses Broadcom (BCM) pin numbering for the GPIO pins, as opposed to physical (BOARD) numbering.
"""
#Change this path if needed. Make sure sendMailV1.py is in this path
from os import chdir
chdir('/home/pi/watcher')


from gpiozero import Button
from gpiozero import LED
#pip install gpiozero
from time import sleep
from ping3 import ping
from datetime import datetime as dt
from sendMailV1 import mailer as mail


mainsCheckPin = 26 #BCM pin26. Change this if you are using a different pin to read AC status
hostPowerPin = 4 #BCM pin4. Change this if you are using a differrent pin to press the Power button.
recipientMailAddress = '' #Change this to the desired recipient for status change alerts
hostIpAddress = '192.168.0.254' #Change this to the host's private IP address
hostName = 'Host'

button = Button(mainsCheckPin) 
hostCtrl = LED(hostPowerPin,active_high=False, initial_value=False) 



def log(txt):
    logFile = 'watcherLogs.log'
    logMsg = '\n'+str(dt.now())+'    ' + str(txt)
    with open(logFile,'a') as f:
        f.write(logMsg)

def mainsOff():
    #Button Gets PRESSED when Mains goes off
    if button.is_pressed: #button.active_time
        sleep(5) # Check after 5 seconds to avoid minor / quick fluctuations
        if button.is_pressed:
            return True # MainsOff = True
    return False

def mainsOn():
    #Button Gets PRESSED when Mains goes off
    if not button.is_pressed: #button.inactive_time
        sleep(5) # Check after 5 seconds to avoid minor / quick fluctuations
        if not button.is_pressed:
            return True # MainsOff = True
    return False

def hostPing():
    for x in range(0,10):
        if bool(ping(hostIpAddress)):
            return True
        sleep(0.5)
    return False

def hostPress():
    hostCtrl.on()
    sleep(0.25)
    hostCtrl.off()

log('Execution Started. Sleeping for 2 minutes to let the internal processes warmup')
sleep(120)
log('Done Sleeping. Starting infinite Loop')

while True:
    hostFlag=False
    if mainsOff():
        if hostPing():
            msg = 'Mains off and '+hostName+ ' On. Putting Host to sleep'
            log(msg)
            mail(recipientMailAddress,'Mains Went Down',hostName+' was On. Putting it to sleep') 
            hostFlag=True
            hostPress()
        else:
            msg = 'Mains off and '+hostName+ ' is already down. No actions on '+hostName
            log(msg)
            mail(recipientMailAddress,'Mains Went Down',hostName+' is already down. No actions') 
            hostFlag=False
        sleep(300) # sleeping for 5 minutes to allow complete shutdown / sleep and avoid flase alarms from fluctuations
        while not mainsOn():
            msg = 'Mains Still off. No actions taken'
            log(msg)
            sleep(300)
        if hostFlag:
            if hostPing():
                msg = 'Mains Came back. '+hostName+ ' was brought down earlier. But it is up now. No actions'
                log(msg)
                mail(recipientMailAddress,'Mains Came back',hostName+' is On already. No actions') 
            else:
                msg = 'Mains Came back. '+hostName+ ' was brought down earlier and it is still down. Powering it back up'
                log(msg)
                hostPress()
                sleep(300) # sleeping for 5 minutes to allow the host to come back up
                if hostPing():
                    msg = 'Mains Came back and mainsChecker flipped '+hostName+ ' Successfully'
                    log(msg)
                    mail(recipientMailAddress,'Mains Came back','mainsChecker flipped '+hostName+ ' Successfully') 
                else:
                    msg = 'Mains Came back and but mainsCheck could not flip '+hostName
                    log(msg)
                    mail(recipientMailAddress,'ALERT!!!! Mains Came back','mainsChecker failed to flip '+hostName) 
        else:
            msg = 'Mains Came back. '+hostName+ ' was already down. No actions'
            log(msg)
            mail(recipientMailAddress,'Mains Came back',hostName+' was already down. No actions') 
    else:
        log('Mains on. No actions required. Sleeping for 5 minutes')
        sleep(300)
        
