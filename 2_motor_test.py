import YB_Pcb_Car
import time

car = YB_Pcb_Car.YB_Pcb_Car()

# Constants
MOTOR_UP_SPEED = 115    ####   65 ~ 125 Speed 
MOTOR_DOWN_SPEED = 0   
DETECT_VALUE = 30   #### 밝기 70/130 


def control_car(direction):
    """
    Control the car based on the decided direction.
    """
    print(f"Controlling car: {direction}")
    if direction == "UP":
        car.Car_Run(MOTOR_UP_SPEED - 35, MOTOR_UP_SPEED - 35)
    elif direction == "LEFT":
        car.Car_Left(MOTOR_DOWN_SPEED, MOTOR_UP_SPEED)
    elif direction == "RIGHT":
        car.Car_Right(MOTOR_UP_SPEED, MOTOR_DOWN_SPEED)
    elif direction == "BACK":
        car.Car_Back(MOTOR_UP_SPEED, MOTOR_UP_SPEED)
    elif direction == "STOP": 
        car.Car_Stop()
    else : 
        car.Car_Stop()
        
        
if __name__ == "__main__":
    control_car("UP")
    time.sleep(2)
    control_car("LEFT")
    time.sleep(2)
    control_car("RIGHT")
    time.sleep(2)
    control_car("BACK")
    time.sleep(2)
    control_car("STOP")
    time.sleep(1)
    
    
