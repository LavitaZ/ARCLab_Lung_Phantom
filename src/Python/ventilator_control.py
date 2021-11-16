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


root = Tk()
data = np.array([])
setp =  np.array([])
lines=[]
root.title('plot')
root.geometry('1000x500')
baudRate = 115200
timesec = np.array([])








#declare lookup table can maybe implement read in python
samples = np.arange(100)
print(samples[-1])
lookup = {
"off" : np.append([2,2,2], 0*samples),


# 0/2pi with samples 0->sin(0) samples->samples
"sine" : np.append([1,1,1], np.sin(2*np.pi*samples/samples[-1]))

 #"saw" : nparray(setpoints[n])
    
}


#find serial port
def findArduino(serial_number):
    for p in serial.tools.list_ports.comports():
        print(p.serial_number)
        if p.serial_number == serial_number:
            return p.device






#-- make mulitple objects for different waveforms
class waveform:
    def __init__(self, name='1', frequency=1, amplitude=1):
        self.kp = lookup[name][0]
        self.kd = lookup[name][1]
        self.ki = lookup[name][2]
        self.setpoints = amplitude*lookup[name][3:]
        self.freq = frequency
        self.period = 1/frequency
        self.initime = time.time()
        #interpolate using full set points. setpoints sin() samples
        self.func = interpolate.splrep(samples,self.setpoints)
        self.setpoint = 0

        
    def calcsetpoint(self):

        # rotates through 0 - period
        timeper = (time.time() - w.initime)%self.period

        #func using setpoint and samples
        self.setpoint = interpolate.splev(timeper * samples[-1]/self.period , self.func)
        #print(self.setpoint)

    def sendblowersignal(self):
        setpointconv= float(self.setpoint)*1024/2 + 541
        s1.write(str(int(setpointconv)).encode('utf-8'))
          
    def setvariables(self, name, frequency, amplitude):
        self.kp = lookup[name][0]
        self.kd = lookup[name][1]
        self.ki = lookup[name][2]
        self.setpoints = amplitude*lookup[name][3:]
        self.freq = frequency
        self.period = 1/frequency
        self.initime = time.time()
        #interpolate using full set points. setpoints sin() samples
        self.func = interpolate.splrep(samples,self.setpoints)
        self.setpoint = 0

    def read_write(self):
        self.calcsetpoint()
        s1.write(str(int(float(self.setpoint)*1024/2 + 541)).encode('utf-8'))
        time.sleep(.05)
        serin = s1.readline()
        serinstring = serin.decode()
        return(serin)


'''
def declare/reset waveform object(waveform)
    self = control waveform(waveentry.get())


'''


'''
needs access
data
button declare object
blower control pwm number
    -comes from data
    -ks
    -setpoint
'''

#real time function
def plot_data():
    global data
    global setp
    global ax
    global timesec
#   global s1
#read in data
    bitdata = w.read_write()
    if bitdata:
        bitstring = bitdata.decode()
        bitnum = (2*(float(bitstring) - 541)/1024)
#create data array and plot

        if len(data) < 100:
                data = np.append(data, bitnum)
                setp = np.append(setp,w.setpoint)
                timesec = np.append(timesec,time.time()- startime)
                lines[0].set_xdata(timesec)
                lines[0].set_ydata(data)
                lines[1].set_xdata(timesec)
                lines[1].set_ydata(setp)
                ax.set_xlim(timesec[0],timesec[-1]+.00001)
                canvas.draw()
                
        else:
                data[0:99] = data[1:100]
                data[99] = bitnum
                setp[0:99] = setp[1:100]
                setp[99] = w.setpoint
                timesec[0:99] = timesec[1:100]
                timesec[99] = time.time()- startime
                lines[0].set_xdata(timesec)
                lines[0].set_ydata(data)
                lines[1].set_xdata(timesec)
                lines[1].set_ydata(setp)
                ax.set_xlim(timesec[0],timesec[99])
                canvas.draw()



# ---------------------------------send blower signal-----------------------------------------------------
#resets setpoint



    root.after(1, plot_data) # run function after a certain time ms




   
#button functions
def b_stop():
    stopcom = '0'
    s1.reset_output_buffer()
    s1.write(stopcom.encode('utf-8'))
    print('stop')

def b_start():
    startcom = '650'
    s1.reset_output_buffer()
    s1.write(startcom.encode('utf-8'))
    print('start')
    print(data)
    print(data.size)
    root.after(1,dataaccess)


def b_set():
    s1.reset_output_buffer()
    amplitude =str(int(float(ampin.get())/2*1024) + 541)
    s1.write(('a' + amplitude).encode('utf-8'))
    print(amplitude)
    time.sleep(.05)
    s1.write(('f' + freqin.get()).encode('utf-8'))
    







# initialize waveform
w = waveform("off",.1,.1)
    


#create figure
fig = Figure()
ax= fig.add_subplot(111)
ax.set_title('Phantom Lung Pressure')
ax.set_xlabel("Time (S)")
ax.set_ylabel("Pressure (in. Psi)")
ax.set_xlim(0,100)
ax.set_ylim(-1,1)
lines.append(ax.plot([], [])[0])
lines.append(ax.plot([],[])[0])
canvas= FigureCanvasTkAgg(fig,master=root)
canvas.get_tk_widget().place(x=10,y=10,width=600,height=400)
canvas.draw()



#----------------------------------- Place Widgets ------------------------------------------------------------------------------------------------------------------------------------------

#place start button

myFont = font.Font(size = 10)
button1 = Button(root, text="start",height =4, width = 16, bg = 'green', command = lambda:b_start())
button1['font'] = myFont
button1.place(x=10, y=420)

#place stop button

button2 = Button(root, text="stop", height =4, width = 16, bg= 'red', command = lambda:b_stop())
button2['font'] = myFont
button2.place(x=470, y=420)

'''
#Set button
setbut = Button(root , text= "set",width= 20, command= lambda: b_set())
setbut.place(x=700, y=160)
''' 





#Entry Labels
amplabel= Label(root, text="Amplitude", font=("Courier 22 bold"))
amplabel.pack()
amplabel.place(x=700, y=10)

freqlabel= Label(root, text="Frequency", font=("Courier 22 bold"))
freqlabel.pack()
freqlabel.place(x=700, y=90)




#Entries

ampin = Entry(root, width= 40)
ampin.focus_set()
ampin.pack()
ampin.place(x=700, y=50)


freqin = Entry(root, width= 40)
freqin.focus_set()
freqin.pack()
freqin.place(x=700, y=130)


#waveform button
sbut = Button(root, text="sine", height =4, width = 16, bg= 'red', command = lambda:w.setvariables("sine",float(freqin.get()),float(ampin.get())))
sbut.place(x=700, y=200)



#serial connnection
teensyserial = '9141150'
port = findArduino(teensyserial)
s1 = serial.Serial(port,baudRate)
s1.reset_input_buffer()

startime = time.time()
root.update()
plot_data() 
root.mainloop()
s1.close()


