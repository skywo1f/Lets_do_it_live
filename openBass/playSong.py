import time
from rpi_ws281x import *
import argparse
#import cello
import testSong as cello

# LED strip configuration:
LED_COUNT      = 16      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

NORMAL_BRIGHT  = 64
tempo = 500



def sumUp(coord,tab):
    thisLayer = 21 - tab
    index = 4*thisLayer + coord
    return index
    

def playNote(index, coord, bright,strip,openNote):
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
            strip.setPixelColor(index,Color(4,bright*8,4)) #green

        if coord == 1:
            strip.setPixelColor(index,Color(4,4,bright*8)) #blue
    
        if coord == 2:
            strip.setPixelColor(index,Color(bright*8,4,4)) #red
        
        if coord == 3:
            strip.setPixelColor(index,Color(bright*8,bright*8,4)) #yellow

    strip.show()

def clearNote(idx,strip):
    strip.setPixelColor(idx, 0)
 
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
 
    if True:
        print("starting song")
        while True:
            for idx in range(cello.songLength):
                current = cello.song[idx]
                thisCoord = current[0]
                thisTab = current[1]
                if thisTab == 21:
                    openNote = True
                else:
                    openNote = False
                if thisCoord < 4 :
                    lightNum = sumUp(thisCoord,thisTab)
                    playNote(lightNum,thisCoord,128,strip,openNote)
                
                nextNote = cello.song[(idx + 1)%cello.songLength]
                nextCoord = nextNote[0]
                nextTab = nextNote[1]
                if nextTab == 21:
                    openNote = True
                else:
                    openNote = False
                if nextTab < 4:
                    nextLight = sumUp(nextCoord,nextTab)
                    playNote(nextLight,thisCoord,4,strip,openNote)
                time.sleep(tempo/1000)
                clearNote(idx,strip)
                clearNote((idx+1)%cello.songLength,strip)
                print("playing index ")
                print(idx)
            time.sleep(10)
    

