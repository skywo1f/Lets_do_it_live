# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 09:00:15 2020

@author: 
"""

import pyautogui as pag
import time

while(True):
    time.sleep(5)                                  #wait for window switch
    pag.click(1805, 194)                            #click on undock
    time.sleep(1)                                   
    pag.click(1805, 194)                            #click undock again, sometimes it doesnt read it
    time.sleep(15)                                  #wait for undock
    pag.click(1600,300,button='right')              #right click on first mining zone 234
    time.sleep(3)
    pag.click(1600,300,button='right')             #a lot of clicks are duplicated in case they arent read
    time.sleep(3)
    pag.click(1528, 98)                                 #click to warp there
    time.sleep(3)
    pag.click(1528, 98)
    time.sleep(30)                                      #wait for warp
    pag.click(1566, 454,button='right')                 #right click on asteroid in menu
    time.sleep(3)
    pag.click(1566, 454,button='right')
    time.sleep(3)
    pag.click(1499, 100)                                #click on approach
    time.sleep(3)
    pag.click(1499, 100)
    time.sleep(60)                                          #wait for approach
    time.sleep(3)
    pag.click(1630, 103)                                    #click on lock on
    time.sleep(3)
    pag.click(1132, 929)                                #first mining laser
    time.sleep(3)
    pag.click(1175, 925)                                #second mining laser
    time.sleep(3)
    pag.click(1175, 925)
    
    time.sleep(1000)                                 #mining time
    
    pag.keyDown('alt')                          #open favorite locations
    pag.keyDown('e')
    time.sleep(1)
    pag.keyUp('alt')
    pag.keyUp('e')
    time.sleep(3)
    pag.click(834, 580,button='right')              #click on home
    time.sleep(3)
    pag.click(834, 580,button='right')
    time.sleep(3)
    pag.moveTo(902, 590)                            #dock at home
    pag.click(902, 590)
    time.sleep(3)
    pag.click(1203, 355)
    time.sleep(3)
    pag.click(1203, 355)                            #close the window
    
    time.sleep(40)                                  #wait for warp to happen
    time.sleep(3)
    pag.click(1718, 488,button='right')             #right click on the space ship
    time.sleep(3)
    pag.click(1718, 488,button='right')
    time.sleep(3)
    pag.moveTo(1803, 613)                           #click on cargo hold
    time.sleep(3)
    pag.click(1803, 613)
    time.sleep(3)
    pag.moveTo(1251, 187)                           
    time.sleep(3)
    pag.mouseDown(x=1251, y=187, button='left')      #drag ore to item hangar
    time.sleep(1)
    pag.moveTo(1135, 210)
    time.sleep(1)
    pag.mouseUp(x=1135, y=210, button='left')
    time.sleep(3)
    pag.click(1629, 79)                                     #close ore window
    time.sleep(3)
    pag.click(1629, 79)
    
















