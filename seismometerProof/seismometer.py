# importing everythin necessary
import numpy as np
import time
import accUtil as acc # accel
import adcUtil as adc # piezo
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO

# use GPIO numbering
GPIO.setmode(GPIO.BCM)
GPIO.setup(25, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # the tilt switch is just a button!

class Accelerometer():
    
    def __init__(self, tref=0):
        if (tref != 0):
            self.tref = tref
        else:
            self.tref = time.time()
            
        self.timer = np.array([])
        self.xAccel = np.array([]) # initialize all empty arrays
        self.yAccel = np.array([])
        self.zAccel = np.array([])
        self.to = time.time() # keep track of the start time for better organization later

    def getTref(self):
        return self.tref # just return the current time

    def setTref(self, tref):
        self.tref = tref # update the time. tref would be the current time

    def read(self):
        ax,ay,az = acc.readACC() # get acceleration data
        self.xAccel = np.append(self.xAccel, ax)
        self.yAccel = np.append(self.yAccel, ay) # sort them in x y z
        self.zAccel = np.append(self.zAccel, az)
        
        self.timer = np.append(self.timer, self.tref-self.to) # take note of time

    def save(self, name=None):
        accelerometerData = [self.timer, self.xAccel, self.yAccel, self.zAccel] # shrink into one array
        np.savez("accelerometerData.npz", accelerometerData) # put all of the data into a file

    def plot(self):
        plt.figure(figsize=(15,5))           
        plt.plot(self.timer, self.xAccel, color='b')
        plt.plot(self.timer, self.yAccel, color = 'y') # make a plot. Literally copied and pasted this from the last HL
        plt.plot(self.timer, self.zAccel, color = 'g')
        plt.xlabel("Time (seconds)")
        plt.ylabel("Acceleration (m/s/s)")
        plt.title("Acceleration in x, y, z")
        plt.legend(["x", "y", "z"])
        
#=====================================================================================================
class PiezoElement():
    def __init__(self, tref=0, chan = 0): # could have interited some of the stuff, but I didn't
        if (tref != 0):
            self.tref = tref
        else:
            self.tref = time.time()
            
        self.chan = 0 # not super sure exactly why this is necessary. I guess if we had more than 1 device on the ADC, it would make it easier to follow
        self.timer = np.array([])
        self.pazo = np.array([]) # get it? cuz p-a-zo...
        self.to = time.time()

    def getTref(self):
        return self.tref # just return the current time

    def setTref(self, tref):
        self.tref = tref    # tref is current time

    def read(self):
        self.pazo = np.append(self.pazo, adc.readADC(channel=self.chan)) # read and append data from ADC
        self.timer = np.append(self.timer, self.tref-self.to)

    def save(self, name=None):
        piezoData = [self.timer, self.pazo] # data into npz
        np.savez("piezoData.npz", piezoData)

    def plot(self):
        plt.figure(figsize=(15,5))           
        plt.plot(self.timer, self.pazo, color='b')
        plt.xlabel("Time (seconds)")
        plt.ylabel("Piezo Voltage")
        plt.title("Piezo Activity")
        plt.legend(["piezo"]) # dont really need a legend but it says to do it!
        
        
        
running = True # boolean to make sure it only runs once
        
        
while (running == True):
    
    if(GPIO.input(25) == 0):
        print("flipped") # to verify that the switch has been flipped. Otherwise there isn't really a way to tell if its working or not.
        activity = Accelerometer() # initialize accelerometer object
        piezo = PiezoElement() # initialize the piezo object
        to = time.time()
        while (activity.getTref() - to < 10): # run for 10 seconds
            #print(activity.getTref()-to)  # troubleshooting
            activity.setTref(time.time()) # update time and collect data
            activity.read()
            piezo.setTref(time.time()) # update time and collect data
            piezo.read()
            
        activity.plot()
        activity.save() # save and plot data
        piezo.plot()
        piezo.save()
        running = False # dont loop again
        
        
# done!
