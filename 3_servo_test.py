#!/usr/bin/env python
# -*- coding: utf-8 -*-

import YB_Pcb_Car  #Import Yahboom car library
import time

car = YB_Pcb_Car.YB_Pcb_Car()

#######  90° arc 
car.Ctrl_Servo(1, 90) #The servo connected to the S1 interface on the expansion board, rotate to 90°
time.sleep(0.5)
    
car.Ctrl_Servo(2, 90) #The servo connected to the S2 interface on the expansion board, rotate to 90°
time.sleep(0.5)


###### 0 arc
car.Ctrl_Servo(1, 0) #The servo connected to the S1 interface on the expansion board, rotate to 0°
time.sleep(0.5)

car.Ctrl_Servo(2, 0) #The servo connected to the S2 interface on the expansion board, rotate to 0°
time.sleep(0.5)

##### 180 arc 
car.Ctrl_Servo(1, 180) #The servo connected to the S1 interface on the expansion board, rotate to 180°
time.sleep(0.5)

car.Ctrl_Servo(2, 180) #The servo connected to the S2 interface on the expansion board, rotate to 180°
time.sleep(0.5)

#######  90° arc 
car.Ctrl_Servo(1, 90) #The servo connected to the S1 interface on the expansion board, rotate to 90°
time.sleep(0.5)
    
car.Ctrl_Servo(2, 90) #The servo connected to the S2 interface on the expansion board, rotate to 90°
time.sleep(0.5)

del car 