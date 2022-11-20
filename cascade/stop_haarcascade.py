import cv2
import numpy as np


file_name = 'stop.jpg'
stop_cascade_name = 'Stop_cascade.xml'


stop_cascade = cv2.CascadeClassifier()



#-- 1. Load the cascades
if not stop_cascade.load(cv2.samples.findFile(stop_cascade_name)):
    print('--(!)Error loading face cascade')
    exit(0)    


###-- 2. 이미지 읽기 

img = cv2.imread(file_name)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
gray = cv2.equalizeHist(gray)

cv2.imshow("img",img)
cv2.imshow("gray",gray)


stops = stop_cascade.detectMultiScale(gray)
for (x,y,w,h) in stops:
    center = (x + w//2, y + h//2)
    img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 3)

print(stops)

(x,y,w,h) = stops[0]


cv2.putText(img,"Stop Sign", (x,y+10), cv2.FONT_HERSHEY_SIMPLEX,0.6,(0,0,255))
  

cv2.imshow("test",img)
cv2.waitKey()