import cv2
import numpy as np

# Haar 캐스케이드 파일 로드
def load_cascade(file_name):
    cascade = cv2.CascadeClassifier()
    if not cascade.load(cv2.samples.findFile(file_name)):
        print('--(!)Error loading cascade')
        exit(0)
    return cascade

# 이미지 읽기 및 전처리
def read_and_preprocess_image(file_name):
    img = cv2.imread(file_name)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.equalizeHist(gray)
    return img, gray

# 정지 표지판 감지
def detect_stops(gray, cascade):
    return cascade.detectMultiScale(gray)

# 사각형 그리기
def draw_rectangles(img, stops):
    for (x, y, w, h) in stops:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)
        cv2.putText(img, "Stop Sign", (x, y+10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255))

# 이미지 표시
def display_images(img, gray):
    cv2.imshow("Original Image", img)
    cv2.imshow("Processed Image", gray)
    cv2.waitKey()
    cv2.destroyAllWindows()

# 메인 함수
def main():
    file_name = 'stop.jpg'
    cascade_name = 'Stop_cascade.xml'

    stop_cascade = load_cascade(cascade_name)
    img, gray = read_and_preprocess_image(file_name)
    stops = detect_stops(gray, stop_cascade)
    draw_rectangles(img, stops)
    display_images(img, gray)

if __name__ == "__main__":
    main()
