# mainsChecker
Check the AC Mains (city powerline) status and power off/sleep/hibernate a host connected to a UPS. 

While a [UPS](https://en.wikipedia.org/wiki/Uninterruptible_power_supply) is an excellent way to keep your computer up and running even during power outages, 
its major use for power-hungry machines is just to ensure graceful shutdown when the power goes off.  
  
This task is quite a simple process if your computer is turned on when you are in front of it.  
  
If you run time taking, compute-heavy tasks like brute force loops, 2D/3D rendering or data pre-processing, your computer might be running one task for hours if not days together.  
And if your power grid is prone to failures and your UPS isn't a mighty one, you might end up losing multiple hours worth of work when the power and then the UPS fails while you were taking that well-deserved nap.  
Waking up only to realize that the 98% completed task has to be started from scratch is a bummer.  

I was in a similar situation and solved it using my Raspberry Pi 3.  
While the solution works on any Raspberry Pi, I recommend using one with an ethernet port and not a Wireless connection for obvious reasons.

#### **Prerequisites:**
* Raspberry Pi
* Two Single channel 5V Relay Driver Circuits
* A power adaptor capable of powering on one of the Relay Drivers
* UPS
* Host you are trying to control
* e-mail address configurable with smtplib for sending alerts  
* [Enable less secure apps in gmail](https://support.google.com/accounts/answer/6010255?hl=en) if you use a Gmail address to send the notifications.

#### **Summary:**
* The Script runs on Raspberry Pi (Powered by UPS)
* Monitors AC Mains
* If AC Mains goes down:
  * If host is up, press its power button (this can powerdown/sleep/hibernate the host based on the Power settings in the host)
  * If host is down already, do nothing
* When AC Mains comes back:
  * If the host had been powered down earlier:
    * Check if it is up now. If it is, do nothing. (User most likely turned the host on manually).  
This is important cause pressing the power button without checking if the host is up could just power it down
    * If it is not up now, press the power button, check its status after 5 minutes and report the status via e-mail.
  * If the host wasn't disturbed earlier, do nothing.  

#### **How is the AC Mains Status checked?**
* Turn on a (5V or 12V) relay driver circuit(A) and enable (high) its Input (Relay Trigger) through an (appropriate voltage) power adaptor connected to AC Mains.
* Connect a GND pin from the Raspberry Pi to the relay's common terminal.
* Connect **GPIO BCM pin#26** to the relay's Normally Open terminal. **If you are using a different pin, change line # 22(mainsCheckPin) in mainsChecker.py**
* The Common and Normally Open terminals can be swapped as we are just shorting the pins.
* When the AC mains is on, the Relay Driver and its trigger are on -> Common connected to Normally Closed -> button not pressed.
* When the AC mains goes down -> Relay Off -> Common connected to Normally Open -> RPi GND connected to GPIO in -> button pressed.  

#### **How is the host machine's button pressed?**  
* Pick another 5V relay driver circuit(B). This is important since the first relay driver will be completely down during a power failure.
* Power this one up through the Raspberry Pi directly.
* Connect **GPIO BCM pin#4** to the relay driver's input (Relay Trigger).**If you are using a different pin, change line # 23 (hostPowerPin) in mainsChecker.py**
* An additional Vcc/Gnd connection won't be necessary in this case.
* Connect the power switch pins from your host's motherboard to the common and Normally Open terminals of the relay.
* The Common and Normally Open terminals can be swapped as we are just shorting the pins.
* When gpio sets this pin to high, the common and Normally Open terminals are shorted for 0.25 seconds, mimicking a power button press.
* **Note:** You can use readily available or custom Y jumper pins to allow connecting your PC's actual power button and the relay terminals in parallel.  

#### **How is the host's status checked?**  
By pinging it's local IP address from the Raspberry Pi (Same local network)

#### **How/Will I be notified ?**  
Through e-mails.

### **Changes Required in the Code:**
* sendMailV1.py:
  * e-mail (gmailaddress) in line #6 and password in line#7
  * smtp configuration in smtplib.SMTP in the mailerActual function (line # 30), if you a different e-mail address provider.
  * **Note:** I have used threading.Thread for the mail sender to avoid delays in the main loop while the e-mail is being sent.
* mainsChecker.py:
  * mainsCheckPin (line #22), if you are using a different pin to check AC mains status
  * hostPowerPin (line #23), if you are using a different pin to press the power button
  * recipientMailAddress (line #24)
  * hostIpAddress (line #25) to your host's local IP address
  * hostName (line #26) if you want to personalize the alert messages
