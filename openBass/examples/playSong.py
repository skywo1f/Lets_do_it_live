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

# Main program logic follows:
if __name__ == '__main__':

    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    lightNum = 0
    nextLight = 0
    if True:
        print("starting song")
        while True:
            for idx in range(cello.songLength):
                vry_pos = readChannel(vrx_channel)
                tempo = vry_pos*5
                current = cello.song[idx]
                thisCoord = current[0]
                thisFret = current[1]
                if thisFret == 0:
                    openNote = True
                    thisFret = thisFret + 1
                else:
                    openNote = False
                if thisCoord < 4 :
                    lightNum = sumUp(thisCoord,thisFret)
                    playNote(lightNum,thisCoord,32,strip,openNote)
                
                nextNote = cello.song[(idx + 1)%cello.songLength]
                nextCoord = nextNote[0]
                nextFret = nextNote[1]
                if nextFret == 0:
                    openNote = True
                    nextFret = nextFret + 1
                else:
                    openNote = False
                if nextCoord < 4:
                    nextLight = sumUp(nextCoord,nextFret)
                    playNote(nextLight,nextCoord,1,strip,openNote)
                time.sleep(tempo/1000)
                clearNote(lightNum,strip)
                clearNote((lightNum + 1)%cello.songLength,strip)
                print("playing coord ", thisCoord)
                print("playing fret ", thisFret) 
            time.sleep(0)
    

