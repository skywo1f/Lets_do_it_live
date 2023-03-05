
#!/usr/bin/env python
import time
import serial
import matplotlib.pyplot as plt
import numpy as np
import RPi.GPIO as GPIO
switch=40
GPIO.setmode(GPIO.BOARD)
GPIO.setup(switch,GPIO.OUT)
GPIO.output(switch,GPIO.HIGH)
time.sleep(0.5)
GPIO.output(switch,GPIO.LOW)
time.sleep(1)

ser = serial.Serial(
        port='/dev/ttyACM0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
counter=0
data = []
notToggle8 = True
while 1:
    while ser.in_waiting:
        print(ser.readline())
        output = ser.readline()
        try:
            array = output.split()
            array = [float(i) for i in array]
            data.append(array)
            if notToggle8:
                print("inputting commands")
                notToggle8 = False
                ser.write(bytes(b"OM"))
                time.sleep(1)
                ser.write("O8".encode())
        except:
            print("bad")
    if len(data) == 100:
        print("gathered data")
        np.savetxt("test.txt",data)
