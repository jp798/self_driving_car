import YB_Pcb_Car
import time

car = YB_Pcb_Car.YB_Pcb_Car()
MOTOR_SPEED = 50

def move_forward(duration=1):
    car.Car_Run(MOTOR_SPEED, MOTOR_SPEED)
    time.sleep(duration)
    car.Car_Stop()

def move_backward(duration=1):
    car.Car_Back(MOTOR_SPEED, MOTOR_SPEED)
    time.sleep(duration)
    car.Car_Stop()

def turn_left(duration=1):
    car.Car_Left(0, MOTOR_SPEED)
    time.sleep(duration)
    car.Car_Stop()

def turn_right(duration=1):
    car.Car_Right(MOTOR_SPEED, 0)
    time.sleep(duration)
    car.Car_Stop()

def spin_left(duration=1):
    car.Car_Spin_Left(MOTOR_SPEED, MOTOR_SPEED)
    time.sleep(duration)
    car.Car_Stop()

def spin_right(duration=1):
    car.Car_Spin_Right(MOTOR_SPEED, MOTOR_SPEED)
    time.sleep(duration)
    car.Car_Stop()

if __name__ == "__main__":
    move_forward()
    move_backward()
    turn_left()
    turn_right()
    spin_left()
    spin_right()
