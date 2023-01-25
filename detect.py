# GNU General Public License <https://www.gnu.org/licenses>
# Micropython code for monitoring power
# Possible improvements:
# 1. use the neopixel on the Lolin ESP32C2 pulse when posting
# 2. use uasyncio to pulse the led as a heartbeat

import os, network, json, ntptime, urequests, utime
from machine import Timer, enable_irq, disable_irq
import config
# Change these to match your unique identifiers
# WiFi
SSID = config.SSID
password = config.PASSWORD
# io.adafruit.com 
user = config.USER
X_AIO_Key = config.X_AIO_KEY
feed = config.FEED
# IFTTT 
key = config.IFTTT_KEY
event = config.EVENT
# set NTP server
ntptime.host = config.NTP_SERVER
def set_time():
   try:
         ntptime.settime()
   except OSError as e:
         print("Failed ntp request - Error: {0}".format(e))
   return utime.mktime(utime.localtime())        
def do_connect():
	wlan = network.WLAN(network.STA_IF) 
	wlan.active(True)
	if not wlan.isconnected():
		print('Connecting to Network...')
                try:
		    wlan.connect(SSID, password)
                except:
                    pass
		while not wlan.isconnected():
			pass
	print('Network Configuration (IP/GW/DNS1/DNS2): ', wlan.ifconfig())
def do_post(current_time):
   headers = {'X-AIO-Key': X_AIO_Key,'Content-Type': 'application/json'}
   url='https://io.adafruit.com/api/v2/'+user+'/feeds/'+feed+'/data.json'
   data = json.dumps({"value": current_time})
   # POST response
   try:
      response = urequests.post(url, headers=headers, data=data)
   except OSError as e:
      print("OS error: {0}".format(e))
      utime.sleep(30)
      pass
   except IndexError as e:
      # See: https://github.com/micropython/micropython-lib/issues/300
      print("Index Error using urequests: {0}".format(e))
      utime.sleep(30)
      pass
   else:
      response.close()

def ifttt_it(current_time):
   url= 'https://maker.ifttt.com/trigger/'+event+'/with/key/'+key
   headers = {'Content-Type': 'application/json'}
   data = json.dumps({"value1": current_time//60}) # in minutes not seconds
   # POST response
   response = None
   while response.status_code != 200 :
      try:
         response = urequests.post(url, headers=headers, data=data)
      except OSError as e:
         print("OS error: {0}".format(e))
         utime.sleep(30)
         pass
      except IndexError as e:
         # This should not occur if we ensure that we are connected to the
         # wireless network...
         # See: https://github.com/micropython/micropython-lib/issues/300
         print("Index Error using urequests: {0}".format(e))
         utime.sleep(30)
         pass
      else:
         response.close()

# Timer for recalibrating NTP once a day
ntp_timer = Timer(0)
ntp_timer.init(period=1000*60*60*24, mode=Timer.PERIODIC, callback=set_time)
ap = network.WLAN(network.AP_IF) # let's make sure we don't boot as an Access Point
ap.active(False)
do_connect()
current_time = set_time()
try :
   f = open('clock', 'r'); last_time = int(f.read()); f.close()
except :
   f = open('clock', 'w'); f.write(str(current_time)); f.close()
   last_time = current_time    # first time run
delta = current_time - last_time
print('Delta:', delta)
if delta > config.DELTA :
   ifttt_it(delta)
while True:
   # post and record current time
   current_time = utime.mktime(utime.localtime()) 
   f = open('clock', 'w'); f.write(str(current_time)); f.close()
   do_post(current_time)
   utime.sleep(config.INTERVAL)
