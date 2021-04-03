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
            print(thisHz)
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
    if index >= 0:
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
    if idx >= 0:
        idx = int(idx)
        strip.setPixelColor(idx, 0)
        strip.show()

nInvaders = 5
invaderSlow = 2
fireSlow = 5
bulletSlow = 1

def initInvader():
    invaderLoc = []
    for i in range(nInvaders):
        counter = i*3
        xLoc = counter%4
        yLoc = int(counter/4)
        invaderLoc.append([xLoc,yLoc])
    return invaderLoc

def invaderMove(invaderLoc):
    for i in range(len(invaderLoc)):
        xLoc =  invaderLoc[i][0]
        yLoc = invaderLoc[i][1]       
        counter = 4*yLoc + xLoc
        counter = counter + 1
        xLoc = counter%4
        yLoc = int(counter/4)
        invaderLoc[i][0] = xLoc
        invaderLoc[i][1] = yLoc
    #return invaderLoc

def displayInv(invaderLoc,strip):
    for i in range(len(invaderLoc)):
        lightIdx = sumUp(invaderLoc[i][0],invaderLoc[i][1])
        playNote(lightIdx,2,16,strip,0)

def displayUser(userLoc,strip):
    lightIdx = sumUp(0,20)              #erase any old pips
    clearNote(lightIdx,strip)
    lightIdx = sumUp(1,20)
    clearNote(lightIdx,strip)
    lightIdx = sumUp(2,20)
    clearNote(lightIdx,strip)
    lightIdx = sumUp(3,20)
    clearNote(lightIdx,strip)
    lightIdx = sumUp(userLoc[0],userLoc[1]) #show user
    playNote(lightIdx,1,16,strip,0)
    

def moveAndFire(thisHz,userLoc,bulletLoc):
    if thisHz < 45 and thisHz > 30:
        userLoc = [0,20]
        bulletLoc.append([0,19])
    if thisHz >= 45 and thisHz < 65:
        userLoc = [1,20]
        bulletLoc.append([1,19])
    if thisHz >= 65 and thisHz < 85:
        userLoc = [2,20]
        bulletLoc.append([2,19])
    if thisHz >= 85:
        userLoc = [3,20]
        bulletLoc.append([3,19])
    return userLoc

def clearLast(lastInvader,strip):
    for i in range(len(lastInvader)):
        lightIdx = sumUp(lastInvader[i][0],lastInvader[i][1])
        clearNote(lightIdx,strip)

def displayBullets(bulletLoc,bType,strip):
    for i in range(len(bulletLoc)):
        lightIdx = sumUp(bulletLoc[i][0],bulletLoc[i][1])
        playNote(lightIdx,bType,16,strip,0)

def invaderFire(invaderLoc,bulletLoc):
    if len(invaderLoc) > 0:
        xLoc = invaderLoc[len(invaderLoc) - 1][0]
        yLoc = invaderLoc[len(invaderLoc) - 1][1] + 1
        bulletLoc.append([xLoc,yLoc])

def advanceBullet(bulletList,bType):
    killBullet = []
    if bType == 1:
        #print("invader ",bulletList)
        for i in range(len(bulletList)):    #their bullets go up
            bulletList[i][1] = bulletList[i][1] + 1 
            if bulletList[i][1] > 20:
                bulletList.pop(i)           
    if bType == 0:
        #print("my ",bulletList)
        for i in range(len(bulletList)):     #my bullets go down
            bulletList[i][1] = bulletList[i][1] - 1 
            if bulletList[i][1] < 0:
                #bulletList.pop(i)
                killBullet.append(i)
        
        for i in range(len(killBullet)):
            bulletList.pop(killBullet[len(killBullet) - i - 1])

def bulletPlayerCollision(userLoc,invaderBullet):
    stillGoing = True
    for i in range(len(invaderBullet) ):
        if invaderBullet[i][1] == 20:
            if invaderBullet[i][0] == userLoc[0]:
                stillGoing = False
            else:
                invaderBullet.pop(i)
                break
    return stillGoing

def bulletInvaderCollision(invaderLoc,myBullet):
    stillGoing = True
    killInvader = []
    killBullet = []
    for i in range(len(myBullet)):
        for j in range(len(invaderLoc)):
            if myBullet[i][0]== invaderLoc[j][0] and myBullet[i][1]== invaderLoc[j][1]:
                killInvader.append(j)
                killBullet.append(i)
                #myBullet.pop(i)
                #invaderLoc.pop(j)

    for i in range(len(killBullet)):
        myBullet.pop(killBullet[len(killBullet) - i - 1])
    for i in range(len(killInvader)):
        #try:
        invaderLoc.pop(killInvader[len(killInvader) - i - 1])
        #except:
        #    stillGoing = False
        if len(invaderLoc) == 0:
            stillGoing = False
            print("you win")
    return stillGoing        

def runGame():
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    localToggle = toggleHz 
    lastTime = time.time()
    bulletTime = time.time()
    invaderLoc = initInvader()
    lastInvader = [] 
    invaderFireTime = time.time()
    displayInv(invaderLoc,strip)
    userLoc = [0,20] 
    myBullet = []
    oldMyBullet = myBullet.copy()
    invaderBullet = []
    oldInvaderBullet = invaderBullet.copy()
    displayUser(userLoc,strip)
    stillGoing = True
    stillGoingDeath = True
    while stillGoing:
        #advance spaceships
        if(time.time() - lastTime > invaderSlow):
            lastTime = time.time()
            lastInvader = invaderLoc[:]
            clearLast(lastInvader,strip)
            invaderMove(invaderLoc)
            displayInv(invaderLoc,strip)
        #advance bullets
        if (time.time() - bulletTime > bulletSlow):
            bulletTime = time.time()
            clearLast(oldInvaderBullet,strip)
            advanceBullet(invaderBullet,1)
            oldInvaderBullet = invaderBullet.copy()
            displayBullets(invaderBullet,3,strip)
            clearLast(oldMyBullet,strip)
            advanceBullet(myBullet,0)
            oldMyBullet = myBullet.copy()
            displayBullets(myBullet,0,strip)
            #check for collisions
        stillGoingDeath = bulletPlayerCollision(userLoc,invaderBullet)
        stillGoing = bulletInvaderCollision(invaderLoc,myBullet)
        #invaders fire
        if(time.time() - invaderFireTime > fireSlow):
            invaderFire(invaderLoc,invaderBullet)
            invaderFireTime = time.time()
        if (stillGoingDeath == False):
            stillGoing = False
            print("you lose")
        #advance player
        if localToggle != toggleHz:
            userLoc = moveAndFire(thisHz,userLoc,myBullet)
            print(userLoc)
            displayUser(userLoc,strip)
#            displayBullets(myBullet,0,strip)
            localToggle = toggleHz
        
        
               
                

# Main program logic follows:
if __name__ == '__main__':

    lightNum = 0
    nextLight = 0
    hzThread = threading.Thread(target=readSerial)
    hzThread.start()

    playThread = threading.Thread(target=runGame)
    playThread.start()

    

