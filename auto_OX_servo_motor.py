#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import YB_Pcb_Car
import threading
import time

# Haar Cascade 모델 로드
o_sign_cascade = cv2.CascadeClassifier('path_to_o_sign_cascade.xml')

# 차량 및 카메라 초기화
car = YB_Pcb_Car.YB_Pcb_Car()
cap = cv2.VideoCapture(0)
cap.set(3, 320)  # 너비 설정
cap.set(4, 240)  # 높이 설정

def detect_o_sign(frame):
    """
    Haar cascade를 사용하여 프레임에서 'O' 신호를 감지합니다.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    o_signs = o_sign_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    for (x, y, w, h) in o_signs:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # 'O' 신호의 중심을 반환합니다.
        return (x + w//2, y + h//2)
    return None

def rotate_servo_to_sign(car, o_sign_position, frame_width):
    """
    'O' 신호를 향해 서보 모터의 방향을 조절합니다.
    """
    if o_sign_position is not None:
        x_center, _ = o_sign_position
        # 'O' 신호의 위치에 따라 서보 모터를 회전시킬 각도를 계산합니다.
        servo_angle = np.interp(x_center, [0, frame_width], [0, 180])
        car.Ctrl_Servo(1, servo_angle)
        car.Ctrl_Servo(2, servo_angle)  # 두 서보 모터 모두 회전시키고자 한다면
        time.sleep(1)  # 서보 모터가 회전할 시간을 기다립니다.

def main():
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("카메라에서 프레임을 읽지 못했습니다.")
                break
            
            # 'O' 신호 감지
            o_sign_position = detect_o_sign(frame)
            
            # 'O' 신호 방향으로 서보 모터 회전
            if o_sign_position:
                rotate_servo_to_sign(car, o_sign_position, frame.shape[1])
                # 'O' 신호 방향으로 차량을 조금씩 움직여 주차합니다.
                # 예를 들어:
                car.Car_Run(80, 80)  # 전진
                time.sleep(2)  # 필요에 따라 시간 조정
                car.Car_Stop()  # 차량 정지
                break  # 주차 후 루프 탈출
            
            cv2.imshow('Frame', frame)
            if cv2.waitKey(1) & 0xFF == 27:  # ESC를 누르면 종료
                break

    except Exception as e:
        print(f"오류 발생: {e}")

    finally:
        car.Car_Stop()
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
