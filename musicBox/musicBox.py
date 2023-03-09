# yellow button = 27
# blue button = 26
# red button = 25
# green button = 24

# Buzzer = 19

# Potentiometer = ch0 adc
# Flex Sensor = ch1 adc

# 

import adcUtil as adc
import numpy as np
import pigpio
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

pi = pigpio.pi(port = 8887)


yPin = 27
bPin = 26
rPin = 25
gPin = 24

playing = True


GPIO.setup(yPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(bPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(rPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(gPin, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)

buzPin = 19

# PWM parameters
freq = 360    # [Hz] frequency
duty = 0.5   #      duty cycle
duration = 5  # [s]  duration

freq = np.empty(1, dtype = int)

t0 = time.time()
while (time.time()-t0 < 10):
    
    if (GPIO.input(yPin)):
        pi.hardware_PWM(buzPin, 740, int(duty * 1e6)) #740
        freq = np.append(freq, 740)
    elif (GPIO.input(bPin)):
        pi.hardware_PWM(buzPin, 659, int(duty * 1e6)) #659
        freq = np.append(freq, 659)
    elif (GPIO.input(rPin)):
        pi.hardware_PWM(buzPin, 554, int(duty * 1e6)) #554
        freq = np.append(freq, 554)
    elif (GPIO.input(gPin)):
        pi.hardware_PWM(buzPin, 494, int(duty * 1e6)) #494
        freq = np.append(freq, 494)
    else:
        pi.hardware_PWM(buzPin, 0, 0)
        freq = np.append(freq, 0)
    time.sleep(0.05)
    
print("Press the red button to stop playback!")
    
while (playing == True):
    for i in range(len(freq)):
        potState = adc.readADC(channel=1)
        flexState = adc.readADC(channel=0)
        if potState < 0.47:
            time.sleep(0.2)
        elif potState < 0.94:
             time.sleep(0.15)
        elif potState < 1.41:
            time.sleep(0.09)
        elif potState < 1.88:
            time.sleep(0.05)
        elif potState < 2.2:
            time.sleep(0.045)
        elif potState < 2.6:
            time.sleep(0.03)
        else:
            time.sleep(0.02)
        if freq[i] == 0:
            pi.hardware_PWM(buzPin, 0, 0)
            continue

        if flexState > 8:
            mult = 2
        elif flexState > 0.7:
            mult = 1.3
        elif flexState < 0.4:
            mult = 0.3
        elif flexState < 0.6:
            mult = 0.5
        else:
            mult = 1
        pi.hardware_PWM(buzPin, int(freq[i]*mult), int(duty * 1e6))
        if (GPIO.input(rPin)):
            print("Red button pressed - Done playing.")
            playing = False
            break
    

    
    
pi.hardware_PWM(buzPin, 0, 0)
pi.stop()
