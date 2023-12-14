import cv2
import numpy as np
import YB_Pcb_Car
import threading
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
MOTOR_UP_SPEED = 115    # 65 ~ 125 Speed
MOTOR_DOWN_SPEED = 70
DETECT_VALUE = 30   # 밝기 70/130

# Haar Cascade 모델 로드
obstacle_cascade = cv2.CascadeClassifier('path_to_obstacle_cascade.xml')
traffic_light_cascade = cv2.CascadeClassifier('path_to_traffic_light_cascade.xml')
sign_cascade = cv2.CascadeClassifier('path_to_sign_cascade.xml')

# Detection functions
def detect_obstacle(frame, control_signals):
    # Your obstacle detection logic here
    pass

def detect_traffic_light(frame, control_signals):
    # Your traffic light detection logic here
    pass

def detect_sign(frame, control_signals):
    # Your sign detection logic here
    pass

# Autonomous driving functions
def process_frame(frame):
    # Your frame processing logic here
    pass

def decide_direction(histogram):
    # Your direction decision logic here
    pass

def control_car(direction):
    # Your car control logic here
    pass

# Main loop
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        control_signals = {'obstacle': False, 'red_light': False, 'stop_sign': False, 'O_sign': False, 'X_sign': False}
        
        # Create threads for detection tasks
        obstacle_thread = threading.Thread(target=detect_obstacle, args=(frame, control_signals))
        traffic_light_thread = threading.Thread(target=detect_traffic_light, args=(frame, control_signals))
        sign_thread = threading.Thread(target=detect_sign, args=(frame, control_signals))

        # Start threads
        obstacle_thread.start()
        traffic_light_thread.start()
        sign_thread.start()

        # Wait for all threads to complete
        # obstacle_thread.join()
        # traffic_light_thread.join()
        # sign_thread.join()

        # Autonomous driving logic
        if control_signals['obstacle']:
            # Obstacle avoidance logic
            pass
        elif control_signals['red_light']:
            # Traffic light reaction logic
            pass
        elif control_signals['O_sign']:
            # 'O' sign parking logic
            pass
        else: 
            # Standard driving logic
            processed_frame = process_frame(frame)
            histogram = np.sum(processed_frame, axis=0)
            direction = decide_direction(histogram)
            control_car(direction)

        # Display the frame for debugging purposes
        cv2.imshow('Frame', frame)

        # Pause/Unpause and Exit logic
        key = cv2.waitKey(1) & 0xFF
        if key == 32:  # Space bar to pause/unpause
            while True:  # Pause loop
                key = cv2.waitKey(1) & 0xFF
                if key == 32:  # Space bar to unpause
                    break
        elif key == 27:  # ESC to quit
            break

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    car.Car_Stop()
    cap.release()
    cv2.destroyAllWindows()
