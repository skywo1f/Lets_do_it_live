import RPi.GPIO as GPIO
import time
import os
import subprocess

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
#os.environ['PATH'] += r"/home/user/Documents/ChromeDriver"
driver = webdriver.Chrome()

BUTTON_PIN = 26

GPIO.setmode(GPIO.BCM)

GPIO.setup(BUTTON_PIN, GPIO.IN,pull_up_down=GPIO.PUD_UP)
while True:
  buttonNotPressed = True
  while buttonNotPressed:
    buttonNotPressed = GPIO.input(BUTTON_PIN)
    time.sleep(.25)
    print(buttonNotPressed)
  print("button pressed")
# subprocess = subprocess.Popen("timeout 10 spchcat", shell = True,stdout=subprocess.PIPE)
# subprocess_return = subprocess.stdout.read()
  words = os.popen("timeout 10 spchcat").read()
  print(words)    

   
  driver.get("https://www.craiyon.com/") #'AI art website'
  driver.implicitly_wait(10)
  driver.maximize_window()
  aiPromptField = driver.find_element(By.ID,"prompt")
  aiPromptField.send_keys(words)
#generateArt = driver.find_element(By.TYPE,"button") #'button to send the text field to generate art'
#'text field that takes in the art generating prompt'

# generateArt.click()

GPIO.cleanup()
