import cv2
import numpy as np

# MobileSSD 모델 로드
net = cv2.dnn.readNetFromCaffe("models/deploy.prototxt", "models/mobilenet_iter_73000.caffemodel")

# 카메라 입력 받기
cap = cv2.VideoCapture(0)

# 카메라 해상도 설정
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# 클래스 ID와 클래스 이름 매핑
class_names = {0: 'background',
               1: 'aeroplane', 2: 'bicycle', 3: 'bird', 4: 'boat',
               5: 'bottle', 6: 'bus', 7: 'car', 8: 'cat', 9: 'chair',
               10: 'cow', 11: 'diningtable', 12: 'dog', 13: 'horse',
               14: 'motorbike', 15: 'person', 16: 'pottedplant',
               17: 'sheep', 18: 'sofa', 19: 'train', 20: 'tvmonitor'}


while True:
    ret, frame = cap.read()
    h, w = frame.shape[:2]

    # 전처리
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

    # 추론
    net.setInput(blob)
    detections = net.forward()


    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:
            class_id = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")

            # 클래스 이름 가져오기
            label = "Label: {} Confidence: {:.2f}".format(class_names.get(class_id, "Unknown"), confidence)
            
            # 사각형 그리기
            cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)
            
            # 텍스트 레이블 적용
            cv2.putText(frame, label, (startX, startY-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)



    # 프레임 표시
    cv2.imshow("MobileSSD", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
