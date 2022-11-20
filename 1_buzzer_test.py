#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)

p = GPIO.PWM(32, 440) 
p.start(50)
try:

    for dc in range(0, 101, 5):
        print ('start_1')
        p.ChangeDutyCycle(dc)
        time.sleep(0.1)
    for dc in range(100, -1, -5):
        p.ChangeDutyCycle(dc)
        print ('start_2')
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
p.stop()
print("Ending")
GPIO.cleanup()