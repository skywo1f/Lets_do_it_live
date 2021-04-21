import time
from rpi_ws281x import *
import argparse
import cello
#import openNotes as cello
#import cello
import spidev
import os

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

#bass info
eString = [41,44,46,49,52,55,58,62,65,69,73,78,82,87,92,98,104,110,117,123,131]
aString = [55,58,62,65,69,73,78,82,87,92,98,104,110,117,123,131,139,147,156,165,175]
dString = [73,78,82,87,92,98,104,110,117,123,131,139,147,156,165,175,185,196,208,220,233]
gString = [98,104,110,117,123,131,139,147,156,165,175,185,196,208,220,233,247,262,277,294,311]


#music info
data = []
times = []

def readChannel(channel):
  val = spi.xfer2([1,(8+channel)<<4,0])
  data = ((val[1]&3) << 8) + val[2]
  return data

def noteToFreq(note):
    freq = (2^(note-69)/12)*440
    return freq

def loadMidi():
    global data
    global times
    f1 = open('dataTrack.txt')
    data = f1.read().split(',')
    data[0] = data[0][1:]
    data[len(data) - 1] = data[len(data)-1][:-2]
    f2 = open('timeTrack.txt')
    times = f2.read().split(',')
    times[0] = times[0][1:]
    times[len(times) - 1] = times[len(times)-1][:-2]

def readChannel(channel):
  val = spi.xfer2([1,(8+channel)<<4,0])
  data = ((val[1]&3) << 8) + val[2]
  return data
 

def sumUp(coord,tab):
    thisLayer = 20 - tab
    index = 4*thisLayer + coord
    return index
    

def playNote(index, coord, bright,strip,openNote):
    index = int(index)
    if not openNote:
        if coord == 0:
            strip.setPixelColor(index,Color(0,bright*NORMAL_BRIGHT,0)) #green

        if coord == 1:
            strip.setPixelColor(index,Color(0,0,bright*NORMAL_BRIGHT)) #blue
    
        if coord == 2:
            strip.setPixelColor(index,Color(bright*NORMAL_BRIGHT,0,0)) #red
        if coord == 3:
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
    idx = int(idx)
    strip.setPixelColor(idx, 0)
    strip.show()

def showNote():
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    loadMidi()
    localToggle = toggleHz
    eNum = -1
    aNum = -1
    dNum = -1
    gNum = -1
    ledSleep = 0.01

    while True:
        for i in range(len(data)):
            vry_pos = readChannel(vrx_channel)
            time.sleep(times[i])
            clearNote(eNum,strip)             #erase the previous note
            time.sleep(ledSleep)
            clearNote(aNum,strip)             #erase the previous note
            time.sleep(ledSleep)
            clearNote(dNum,strip)             #erase the previous note
            time.sleep(ledSleep)
            clearNote(gNum,strip)             #erase the previous note
            time.sleep(ledSleep)
            thisHz = noteToFreq(data[i])
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
 


   # Main program logic follows:
if __name__ == '__main__':

    playThread = threading.Thread(target=showNote)
    playThread.start()



