import YB_Pcb_Car  #Import Yahboom car library
import time

car = YB_Pcb_Car.YB_Pcb_Car()

MOTOR_SPEED = 100

#### UP
car.Car_Run(MOTOR_SPEED, MOTOR_SPEED) #### 0 ~ 150 
time.sleep(3)
car.Car_Stop()


##### DOWN
car.Car_Back(MOTOR_SPEED, MOTOR_SPEED)
time.sleep(3)
car.Car_Stop()


#### LEFT
car.Car_Left(0, MOTOR_SPEED)
time.sleep(2)
car.Car_Stop()

#### RIGHT 
car.Car_Right(MOTOR_SPEED, 0)
time.sleep(2)
car.Car_Stop()

#### SPIN_LEFT
car.Car_Spin_Left(MOTOR_SPEED, MOTOR_SPEED)
time.sleep(2)
car.Car_Stop()


### SPIN_RIGHT
car.Car_Spin_Right(MOTOR_SPEED, MOTOR_SPEED)
time.sleep(2)
car.Car_Stop()
