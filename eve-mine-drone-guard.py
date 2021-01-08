# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 09:00:15 2020

@author: 
"""

import pyautogui as pag
import time


while(True):
    time.sleep(5)                                  #wait for window switch
    pag.moveTo(1713, 213)
    time.sleep(1)
    pag.click(1713, 213)                            #click on undock
    time.sleep(15)                                  #wait for undock
    pag.click(1431, 438,button='right')              #right click on first mining zone 234
    time.sleep(3)
    pag.click(1431, 438,button='right')             #a lot of clicks are duplicated in case they arent read
    time.sleep(3)
    pag.moveTo(1531, 455)
    time.sleep(3)
    pag.click(1531, 455)                                 #click to warp there
    time.sleep(30)                                      #wait for warp
    time.sleep(3)
    
    time.sleep(3)
    pag.keyDown('shift')                          #open inventory 
    pag.keyDown('f')
    time.sleep(1)
    pag.keyUp('shift')
    pag.keyUp('f')
    time.sleep(3)
    
    time.sleep(3)
    pag.click(1429, 518)                 #right click on asteroid in menu
    time.sleep(3)
    pag.click(1429, 518)
    time.sleep(3)
    pag.click(1562, 120)                                #click on orbit
    time.sleep(3)
    pag.click(1562, 120)
    time.sleep(40)                                          #wait for approach
    time.sleep(3)    
    pag.click(1627, 121)                                    #click on lock on
    time.sleep(3)
    pag.click(1072, 903)                                #first mining laser
    time.sleep(3)
    pag.click(1122, 897)                                #second mining laser
    time.sleep(3)
    pag.click(1122, 897)                                #second mining laser
    
    time.sleep(500)                                 #mining time
    
    time.sleep(3)
    pag.keyDown('shift')                          #open inventory 
    pag.keyDown('r')
    time.sleep(1)
    pag.keyUp('shift')
    pag.keyUp('r')
    time.sleep(3)    
    
    time.sleep(5)
    pag.click(1496,831,button='right')              #click on home
    time.sleep(3)
    pag.click(1496, 831,button='right')
    time.sleep(3)
    pag.moveTo(1620, 796)                            #dock at home
    pag.click(1620, 796)
    time.sleep(50)                                  #wait for warp and dock to happen
   
    time.sleep(3)
    pag.keyDown('alt')                          #open inventory 
    pag.keyDown('c')
    time.sleep(1)
    pag.keyUp('alt')
    pag.keyUp('c')
    time.sleep(3)
    
    pag.click(145, 403)                           #click on cargo hold
    time.sleep(3)
    pag.click(145, 403)                           #click on cargo hold
    time.sleep(3)   

    pag.moveTo(257, 436)                           
    time.sleep(3)
    pag.mouseDown(x=257, y=436, button='left')      #drag ore to item hangar
    time.sleep(1)
    pag.moveTo(109, 451)
    time.sleep(1)
    pag.mouseUp(x=109, y=451, button='left')
    time.sleep(3)
    pag.click(627, 318)                                     #close ore window
    time.sleep(3)
    pag.click(1629, 79)
    
















