import cv2
import threading
import copy

# Haar Cascade 모델 로드
obstacle_cascade = cv2.CascadeClassifier('path_to_obstacle_cascade.xml')
traffic_light_cascade = cv2.CascadeClassifier('path_to_traffic_light_cascade.xml')
sign_cascade = cv2.CascadeClassifier('path_to_sign_cascade.xml')

# 카메라 설정
cap = cv2.VideoCapture(0)

# 각 객체를 인식하는 함수
def detect_obstacle(frame, output):
    obstacles = obstacle_cascade.detectMultiScale(frame, 1.3, 5)
    for (x,y,w,h) in obstacles:
        cv2.rectangle(output,(x,y),(x+w,y+h),(255,0,0),2)

def detect_traffic_light(frame, output):
    traffic_lights = traffic_light_cascade.detectMultiScale(frame, 1.3, 5)
    for (x,y,w,h) in traffic_lights:
        cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),2)

def detect_sign(frame, output):
    signs = sign_cascade.detectMultiScale(frame, 1.3, 5)
    for (x,y,w,h) in signs:
        cv2.rectangle(output,(x,y),(x+w,y+h),(0,0,255),2)

# 메인 루프
while True:
    ret, original_frame = cap.read()
    if not ret:
        break

    # 스레드에서 사용할 프레임 복사본
    frame_obstacle = copy.deepcopy(original_frame)
    frame_traffic_light = copy.deepcopy(original_frame)
    frame_sign = copy.deepcopy(original_frame)

    # 스레드 생성 및 실행
    obstacle_thread = threading.Thread(target=detect_obstacle, args=(frame_obstacle, original_frame))
    traffic_light_thread = threading.Thread(target=detect_traffic_light, args=(frame_traffic_light, original_frame))
    sign_thread = threading.Thread(target=detect_sign, args=(frame_sign, original_frame))

    obstacle_thread.start()
    traffic_light_thread.start()
    sign_thread.start()

    # 스레드 종료 대기
    obstacle_thread.join()
    traffic_light_thread.join()
    sign_thread.join()

    # 결과 표시
    cv2.imshow('Frame', original_frame)

    # 'q'를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
