import time
from rpi_ws281x import *
import argparse
import cello
#import openNotes as cello
#import cello
import spidev
import os
import serial
import threading

ser = serial.Serial(
	port='/dev/ttyACM0',
	baudrate= 9600,
	parity = serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS,
	timeout=1
)

thisHz = 0
toggleHz = 0

def readSerial():
    global thisHz
    global toggleHz
    while True:
        while ser.in_waiting:
            tempHz = ser.readline()
            thisHz = int(tempHz[:-5])
            toggleHz = (toggleHz + 1)%2

# LED strip configuration:
LED_COUNT      = 80      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

NORMAL_BRIGHT  = 4
tempo = 2500

swt_channel = 0
vrx_channel = 1
vry_channel = 2

# Spi oeffnen
spi = spidev.SpiDev()
spi.open(0,0)
spi.max_speed_hz=1000000

eString = [41,44,46,49,52,55,58,62,65,69,73,78,82,87,92,98,104,110,117,123,131]
aString = [55,58,62,65,69,73,78,82,87,92,98,104,110,117,123,131,139,147,156,165,175]
dString = [73,78,82,87,92,98,104,110,117,123,131,139,147,156,165,175,185,196,208,220,233]
gString = [98,104,110,117,123,131,139,147,156,165,175,185,196,208,220,233,247,262,277,294,311]

 

def sumUp(coord,tab):
    thisLayer = 20 - tab
    index = 4*thisLayer + coord
    return index
    

def playNote(index, coord, bright,strip,openNote):
#    index = int(index)
#    bright = 32
    print("coord is ",coord)
    if index >= 0:
        if not openNote:
            if coord == 0:
                strip.setPixelColor(index,Color(0,bright*NORMAL_BRIGHT,0)) #green
            if coord == 1:
                strip.setPixelColor(index,Color(0,0,bright*NORMAL_BRIGHT)) #blue
            if coord == 2:
 #               print("playing red note with index ", index)
                strip.setPixelColor(index,Color(bright*NORMAL_BRIGHT,0,0)) #red
            if coord == 3:
#                print("playing yellow note with index ",index)
                strip.setPixelColor(index,Color(bright*NORMAL_BRIGHT,bright*NORMAL_BRIGHT,0)) #yellow
        else:
            if coord == 0:
                strip.setPixelColor(index,Color(14,bright*2,14)) #green

            if coord == 1:
                strip.setPixelColor(index,Color(14,14,bright*2)) #blue
        
            if coord == 2:
                strip.setPixelColor(index,Color(bright*2,14,14)) #red
            
            if coord == 3:
                strip.setPixelColor(index,Color(bright*2,bright*2,14)) #yellow

        strip.show()

def clearNote(idx,strip):
    if idx > 0:
        idx = int(idx)
        strip.setPixelColor(idx, 0)
        strip.show()


def showNote(): 
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    localToggle = toggleHz
    eNum = -1
    aNum = -1
    dNum = -1
    gNum = -1
    ledSleep = 0.01 
    while True:
        if localToggle != toggleHz:
            clearNote(eNum,strip)             #erase the previous note
            time.sleep(ledSleep)
            clearNote(aNum,strip)             #erase the previous note
            time.sleep(ledSleep)
            clearNote(dNum,strip)             #erase the previous note
            time.sleep(ledSleep)
            clearNote(gNum,strip)             #erase the previous note
            time.sleep(ledSleep)
            localToggle = toggleHz
            print(thisHz)
#            test = sumUp(3,5)
#            playNote(test,3,64,strip,False)
            for i in range(len(eString) - 1):
                if (thisHz >= eString[i] and thisHz < eString[i + 1]):
                    eNum = sumUp(0,i)                 #grab the light location
                    if not i:
                        eNum = eNum + 1
                    playNote(eNum,0,16,strip,not i)
                    time.sleep(ledSleep)                    #give the led a chance to light up
                if (thisHz >= aString[i] and thisHz < aString[i + 1]):
                    aNum = sumUp(1,i)
                    if not i:
                        aNum = aNum + 1
                    playNote(aNum,1,16,strip,not i)
                    time.sleep(ledSleep)
                if (thisHz >= dString[i] and thisHz < dString[i + 1]):
                    dNum = sumUp(2,i)
                    if not i:
                        dNum = dNum + 1
                    playNote(dNum,2,16,strip,not i)
                    time.sleep(ledSleep)
                if (thisHz >= gString[i] and thisHz < gString[i + 1]):
                    gNum = sumUp(3,i)
                    if not i:
                        gNum = gNum + 1
                    playNote(gNum,3,16,strip,not i)
                    time.sleep(ledSleep)
               
                

# Main program logic follows:
if __name__ == '__main__':

    lightNum = 0
    nextLight = 0
    hzThread = threading.Thread(target=readSerial)
    hzThread.start()

    playThread = threading.Thread(target=showNote)
    playThread.start()

    

