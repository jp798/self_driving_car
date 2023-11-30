#!/usr/bin/env python
# -*- coding: utf-8 -*-

import YB_Pcb_Car
import time

def initialize_car():
    return YB_Pcb_Car.YB_Pcb_Car()

def rotate_servo(car, servo_id, angle, duration=2):
    """
    Rotate a specific servo to a given angle.

    Args:
    - car: The car object to control.
    - servo_id: The ID of the servo (1 or 2).
    - angle: The angle to rotate the servo to.
    - duration: Time to wait after rotation (default 0.5 seconds).
    """
    car.Ctrl_Servo(servo_id, angle)
    time.sleep(duration)

def rotate_servo_slowly(car, servo_id, target_angle, step=1, step_delay=0.05):
    """
    Rotate a specific servo to a given angle slowly.

    Args:
    - car: The car object to control.
    - servo_id: The ID of the servo (1 or 2).
    - target_angle: The target angle to rotate the servo to.
    - step: The angle increment for each step (default 1 degree).
    - step_delay: Time to wait after each small rotation step (default 0.05 seconds).
    """
    current_angle = 90  # Assuming the servo starts at 90 degrees. Adjust as necessary.

    # Determine the direction of rotation
    step = step if target_angle > current_angle else -step

    for angle in range(current_angle, target_angle, step):
        car.Ctrl_Servo(servo_id, angle)
        time.sleep(step_delay)

    # Ensure the final position is accurately set
    car.Ctrl_Servo(servo_id, target_angle)
    time.sleep(step_delay)

def main():
    car = initialize_car()

    # Rotate servos to 90 degrees
    rotate_servo_slowly(car, 1, 90)
    rotate_servo_slowly(car, 2, 90)

    # Rotate servos to 0 degrees
    rotate_servo_slowly(car, 1, 0)
    rotate_servo_slowly(car, 2, 0)

    # Rotate servos to 180 degrees
    rotate_servo_slowly(car, 1, 180)
    rotate_servo_slowly(car, 2, 180)

    # Rotate servos back to 90 degrees
    rotate_servo_slowly(car, 1, 90)
    rotate_servo_slowly(car, 2, 90)

    del car

if __name__ == "__main__":
    main()
