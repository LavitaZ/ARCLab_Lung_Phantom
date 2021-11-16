import serial
import serial.tools.list_ports
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tkinter.ttk import Frame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.animation as animation
import numpy as np
import time
import tkinter.font as font
from scipy import interpolate
# this is a loop back test

baudRate = 115200

#find serial port
def findArduino(serial_number):
    for p in serial.tools.list_ports.comports():
        print(p.serial_number)
        if p.serial_number == serial_number:
            return p.device



teensyserial = '9141150'
port = findArduino(teensyserial)
s1 = serial.Serial(port,baudRate)
s1.reset_input_buffer()

for i in range(100000000000):
    out = 100*np.sin(2*np.pi*i/1000)

    s1.write(str(out).encode('utf-8'))
    time.sleep(.05)
    serin = s1.readline()
    serinstring = serin.decode()
    print(serinstring)
    
 
