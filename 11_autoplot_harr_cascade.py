import cv2
import numpy as np
import YB_Pcb_Car
import threading
import time

# Camera and car initialization
cap = cv2.VideoCapture(0)
cap.set(3, 320)  # Set width
cap.set(4, 240)  # Set height
cap.set(cv2.CAP_PROP_BRIGHTNESS, 40)
cap.set(cv2.CAP_PROP_CONTRAST, 40)
cap.set(cv2.CAP_PROP_SATURATION, 20)
cap.set(cv2.CAP_PROP_GAIN, 20)

car = YB_Pcb_Car.YB_Pcb_Car()

# Constants
MOTOR_UP_SPEED = 115    # Speed range: 65 ~ 125
MOTOR_DOWN_SPEED = 70
DETECT_VALUE = 30        # Brightness value range: 70/130

# Haar Cascade models
obstacle_cascade = cv2.CascadeClassifier('path_to_obstacle_cascade.xml')
traffic_light_cascade = cv2.CascadeClassifier('path_to_traffic_light_cascade.xml')
sign_cascade = cv2.CascadeClassifier('path_to_sign_cascade.xml')

# Detection functions
def detect_obstacle(frame, control_signals):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    obstacles = obstacle_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    for (x, y, w, h) in obstacles:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    control_signals['obstacle'] = len(obstacles) > 0

def detect_traffic_light(frame, control_signals):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    traffic_lights = traffic_light_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    for (x, y, w, h) in traffic_lights:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
    control_signals['red_light'] = len(traffic_lights) > 0

def detect_sign(frame, control_signals):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    signs = sign_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    for (x, y, w, h) in signs:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    # Assuming the first detected sign is the one we're interested in
    control_signals['sign'] = 'O' if signs else 'X'

# Autonomous driving functions
def process_frame(frame):
    # Convert to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Edge detection
    edges = cv2.Canny(gray_frame, 50, 150)
    # ROI
    roi = edges[120:, :]  # Adjust the slicing according to your needs
    return roi

def decide_direction(roi):
    # Calculate histogram of the ROI
    histogram = np.sum(roi, axis=0)
    midpoint = np.int(histogram.shape[0] / 2)
    leftx_base = np.argmax(histogram[:midpoint])
    rightx_base = np.argmax(histogram[midpoint:]) + midpoint

    # Decide direction based on the histogram
    if leftx_base < midpoint / 2:
        return 'LEFT'
    elif rightx_base > midpoint + (midpoint / 2):
        return 'RIGHT'
    else:
        return 'STRAIGHT'

def control_car(direction):
    if direction == 'LEFT':
        car.Car_Left(MOTOR_DOWN_SPEED, MOTOR_UP_SPEED)
    elif direction == 'RIGHT':
        car.Car_Right(MOTOR_UP_SPEED, MOTOR_DOWN_SPEED)
    elif direction == 'STRAIGHT':
        car.Car_Run(MOTOR_UP_SPEED, MOTOR_UP_SPEED)

# Main loop
try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to read frame from camera.")
            break

        # Shared control signals dictionary
        control_signals = {'obstacle': False, 'red_light': False, 'sign': None}

        # Create and start threads for detection tasks
        obstacle_thread = threading.Thread(target=detect_obstacle, args=(frame, control_signals))
        traffic_light_thread = threading.Thread(target=detect_traffic_light, args=(frame, control_signals))
        sign_thread = threading.Thread(target=detect_sign, args=(frame, control_signals))

        obstacle_thread.start()
        traffic_light_thread.start()
        sign_thread.start()

        # Wait for threads to finish
        # obstacle_thread.join()
        # traffic_light_thread.join()
        # sign_thread.join()

        # Autonomous driving logic based on detections
        if control_signals['obstacle']:
            print("Obstacle detected! Avoiding...")
            control_car('LEFT')  # Change to your obstacle avoidance strategy
        elif control_signals['red_light']:
            print("Red light detected! Stopping...")
            car.Car_Stop()  # Stop the car
        elif control_signals['sign'] == 'O':
            print("Sign 'O' detected! Parking...")
            car.Car_Stop()  # Implement your parking strategy
        else:
            roi = process_frame(frame)
            direction = decide_direction(roi)
            control_car(direction)

        cv2.imshow('Frame', frame)

        # Pause/Unpause and Exit logic
        key = cv2.waitKey(1) & 0xFF
        if key == 32:  # Space bar to pause/unpause
            cv2.waitKey(0)  # Wait until any key is pressed
        elif key == 27:  # ESC to quit
            break

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    car.Car_Stop()
    cap.release()
    cv2.destroyAllWindows()
