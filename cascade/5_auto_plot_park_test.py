import cv2
import time
import numpy as np
import YB_Pcb_Car  #Import Yahboom car library

# 카메라 초기화
def initialize_camera():
    cap = cv2.VideoCapture(0)
    cap.set(3, 320)  # set Width
    cap.set(4, 240)  # set Height
    cap.set(cv2.CAP_PROP_BRIGHTNESS, 45)
    cap.set(cv2.CAP_PROP_CONTRAST, 90)
    cap.set(cv2.CAP_PROP_SATURATION, 20)
    cap.set(cv2.CAP_PROP_GAIN, 20)
    return cap

# 자동차 초기화
def initialize_car():
    car = YB_Pcb_Car.YB_Pcb_Car()
    return car

# 장애물 감지
def detect_obstacle(frame, cascade):
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    obstacles = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in obstacles:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, "Obstacle", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        cv2.imshow('detect_obstacle',frame)
        return True

    return False

# 주차 표지판 감지 및 표시
def detect_and_display_sign(frame, cascade):
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    traffic_sign = cascade.detectMultiScale(gray)
    for (x, y, w, h) in traffic_sign:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        cv2.putText(frame, "Park OK(sign)", (x - 20, y + h + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255))
    cv2.imshow("0.Park OK(sign)", frame)

# 주요 루프
def main_loop(cap, car, traffic_cascade):
    count = 0
    while True:
        ret, frame = cap.read()
        
        if detect_obstacle(frame, traffic_cascade):
            # 장애물이 감지되면 왼쪽으로 이동
            car.Car_Left(MOTOR_DOWN_SPEED, MOTOR_UP_SPEED)
        else:
            # 계속 직진
            car.Car_Run(MOTOR_UP_SPEED, MOTOR_UP_SPEED)

        # 주차 표지판 감지 및 표시
        detect_and_display_sign(frame, traffic_cascade)

        k = cv2.waitKey(30) & 0xff
        if k == 27:  # ESC 키를 누르면 종료
            break
        elif k == 32 : 
            print("./save_images/save_"+str(count)+".jpg")
            cv2.imwrite("./save_images/save_"+str(count)+".jpg", frame)
            count += 1

# 글로벌 변수
MOTOR_UP_SPEED = 70
MOTOR_DOWN_SPEED = 40

if __name__ == "__main__":
    cap = initialize_camera()
    car = initialize_car()
    traffic_cascade = cv2.CascadeClassifier(cv2.samples.findFile('cascade.xml'))  # 캐스케이드 로드
    try:
        main_loop(cap, car, traffic_cascade)
    except Exception as e:
        print("error:", e)
    finally:
        car.Car_Stop()
        cap.release()
        cv2.destroyAllWindows()
