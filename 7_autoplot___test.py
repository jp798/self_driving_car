import cv2
import numpy as np
import YB_Pcb_Car
import random
import time

# Camera and car initialization
cap = cv2.VideoCapture(0)
cap.set(3, 320)  # set Width
cap.set(4, 240)  # set Height
cap.set(cv2.CAP_PROP_BRIGHTNESS, 40)
cap.set(cv2.CAP_PROP_CONTRAST, 40)
cap.set(cv2.CAP_PROP_SATURATION, 20)
cap.set(cv2.CAP_PROP_GAIN, 20)

car = YB_Pcb_Car.YB_Pcb_Car()

# Constants
MOTOR_UP_SPEED = 115    ####   65 ~ 125 Speed 
MOTOR_DOWN_SPEED = 70   
DETECT_VALUE = 30   #### 밝기 70/130 

def process_frame(frame):
    """
    Process the frame to detect edges and transform perspective.
    """
    # Define region for perspective transformation
    
    pts_src = np.float32([[10, 80], [310, 80], [310, 10], [10, 10]])
    pts_dst = np.float32([[0, 240], [320, 240], [320, 0], [0, 0]])


    # 사각형 그리기
    pts = pts_src.reshape((-1, 1, 2)).astype(np.int32)  # np.float32에서 np.int32로 변경
    frame = cv2.polylines(frame, [pts], isClosed=True, color=(0, 0, 255), thickness=2)
    cv2.imshow('1_Frame', frame)

    # Apply perspective transformation
    mat_affine = cv2.getPerspectiveTransform(pts_src, pts_dst)
    frame_transformed = cv2.warpPerspective(frame, mat_affine, (320, 240))
    cv2.imshow('2_frame_transformed', frame_transformed)

    # Convert to grayscale and apply binary threshold
    gray_frame = cv2.cvtColor(frame_transformed, cv2.COLOR_RGB2GRAY)
    cv2.imshow('3_gray_frame', gray_frame)
    _, binary_frame = cv2.threshold(gray_frame, DETECT_VALUE, 255, cv2.THRESH_BINARY)
    return binary_frame

def decide_direction(histogram):
    """
    Decide the driving direction based on histogram.
    """
    left = int(np.sum(histogram[:int(len(histogram) / 4)]))
    right = int(np.sum(histogram[int(3 * len(histogram) / 4):]))
    up = np.sum(histogram[int(len(histogram) / 4):int(3 * len(histogram) / 4)])

    print("left:", left)
    print("right:", right)
    print("up:", up)

    if abs(right - left) > 1000:
        return "LEFT" if right > left else "RIGHT"
    elif up < 10000:
        return "UP"
    else:
        return "UP"

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
    elif direction == "RANDOM":
        random_direction = random.choice(["LEFT", "RIGHT"])
        control_car(random_direction)    

def rotate_servo(servo_id, angle):
    car.Ctrl_Servo(servo_id, angle)    

try:
    rotate_servo(1, 90)  # Rotate servo at S1 to 90 degrees
    rotate_servo(2, 110)  

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame from camera.")
            break

        
        processed_frame = process_frame(frame)
        histogram = np.sum(processed_frame, axis=0)
        print(f"Histogram: {histogram}")
        direction = decide_direction(histogram)
        print(f"Decided direction: {direction}")
        control_car(direction)

        # Display the processed frame (for debugging)
        cv2.imshow('4_Processed Frame', processed_frame)
        

        key = cv2.waitKey(30) & 0xff
        if key == 27:  # press 'ESC' to quit
            break
        elif key == 32:  # press 'Space bar' for pause and debug
            print("Paused for debugging. Press any key to continue.")
            cv2.waitKey()

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    car.Car_Stop()
    cap.release()
    cv2.destroyAllWindows()
