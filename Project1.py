import urllib.request
import urllib.parse
import json
import re
import pip._vendor.requests
import smtplib
import time

urlBase = "https://cn.wio.seeed.io/v1/node/"
air = "GroveAirqualityA0/quality?"
barOr = "GroveLEDBarUART0/orientation/1?"
barLevel = "GroveLEDBarUART0/level/"

level = 0    
red = 0
blue = 0                                                       #change this to interpolate LEDbar value
LEDbar = f"GroveLEDBarUART0/toggle/"                        #might need to update this in loop
LEDbaseRed = "GenericDOutD1/onoff/" 
LEDbaseBlue = "GenericDOutD0/onoff/"                            
access_token = "access_token=c23b344babb5c5f82f3231dc9d96fe22"

#for the air quality sensor, I had it as >1000 = clean because i put an alcohol pad over it and it registered as 700 while normally it registered over 1000

counter = 0
notDrunk = True



while notDrunk:

    #counter += 1
    #red = counter%2
    #blue = (counter+1)%2
    #level = counter%10
    #print(counter)
    #pip._vendor.requests.post(urlBase+LEDbase+str(red)+"?"+access_token)
    #pip._vendor.requests.post(urlBase+LEDbase+str(blue)+"?"+access_token)
    #pip._vendor.requests.post(urlBase+LEDbar+str(level)+"?"+access_token)
    #time.sleep(1)


    quality = urllib.request.urlopen(urlBase+air+access_token).read()
    quality = json.loads(quality)
    quality = str(quality)
    quality = int(re.search(r'\d+',quality).group())
    print("Air quality: "+str(quality))
    
    level = 10-(float(quality)/100)
    if level > 3:
        notDrunk = False
    
   
    
    pip._vendor.requests.post(urlBase+barOr+access_token)
    pip._vendor.requests.post(urlBase+barLevel+str(level)+"%0A?"+access_token) #0A lets me use decimal point in number
    if quality > 1000:
        pip._vendor.requests.post(urlBase+LEDbaseBlue+"1?"+access_token)
        pip._vendor.requests.post(urlBase+LEDbaseRed+"0?"+access_token)
        print("Air is clean.")
    else:
        pip._vendor.requests.post(urlBase+LEDbaseRed+"1?"+access_token)
        pip._vendor.requests.post(urlBase+LEDbaseBlue+"0?"+access_token)
        print("Alcohol detected.")
        clean = False






