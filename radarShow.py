from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
time.sleep(60)
#driver = webdriver.Firefox()
while True:
    driver = webdriver.Chrome()
    driver.get("https://radar.weather.gov/?settings=v1_eyJhZ2VuZGEiOnsiaWQiOiJ3ZWF0aGVyIiwiY2VudGVyIjpbLTg1Ljc5MSwzOS42MDNdLCJ6b29tIjo4LCJsb2NhdGlvbiI6Wy04Ni45MTMsMzkuNDddfSwiYW5pbWF0aW5nIjp0cnVlLCJiYXNlIjoic3RhbmRhcmQiLCJhcnRjYyI6ZmFsc2UsImNvdW50eSI6ZmFsc2UsImN3YSI6ZmFsc2UsInJmYyI6ZmFsc2UsInN0YXRlIjpmYWxzZSwibWVudSI6dHJ1ZSwic2hvcnRGdXNlZE9ubHkiOmZhbHNlLCJvcGFjaXR5Ijp7ImFsZXJ0cyI6MC42LCJsb2NhbCI6MC42LCJsb2NhbFN0YXRpb25zIjowLjgsIm5hdGlvbmFsIjowLjZ9fQ%3D%3D#/")
    driver.maximize_window()
    time.sleep(300)
    driver.close()

#time.sleep(20)
#elem = driver.find_element_by_class_name("play-bar-toggle")
#elem.click()
#driver.close()
