#!/usr/bin/env python
import time
import serial
import matplotlib.pyplot as plt

ser = serial.Serial(
        port='/dev/ttyACM0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
)
counter=0

while 1:
    while ser.in_waiting:
        print(ser.readline())
        output = ser.readline()
        array = output.split()
        array = [float(i) for i in array]
        #print(array)
        plt.plot(array)
        plt.show()
