import pyautogui
import webbrowser
import time
if __name__ == "__main__":
#       webbrowser.open('https://weather.com/weather/radar/interactive/l/38776f9e115b495a6d091b50419be4a10f074920d58d3ab0c95aff77616b383d')
        webbrowser.open('https://www.accuweather.com/en/us/indiana/weather-radar')
        time.sleep(45)
        pyautogui.click(x=1357, y=237)
        time.sleep(5)
        pyautogui.click(x=780, y=350)
        time.sleep(5)
        pyautogui.click(x=505, y=650)

        while True:
                time.sleep(300)
                pyautogui.click(x=1342, y=22)
                time.sleep(5)
                webbrowser.open('https://www.accuweather.com/en/us/indiana/weather-radar')
                time.sleep(20)
                pyautogui.click(x=1357, y=237)
                time.sleep(5)
                pyautogui.click(x=780, y=350)
                time.sleep(5)
                pyautogui.click(x=505, y=650)







#remove the adds
#Point(x=1005, y=294)
#fullscreen the map
#Point(x=87, y=694)
#play the animation
#Point(x=563, y=675)
#pyautogui.position()
#pyautogui.click(x=763,y=671)
