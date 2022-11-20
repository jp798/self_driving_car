import cv2
import time
import enum
import numpy as np 

cap = cv2.VideoCapture(0)
cap.set(3,640) # set Width
cap.set(4,480) # set Height


while True : 

    ret, frame = cap.read()


    Source = np.float32([[40, 145],  [360, 145], [10, 195], [390, 195]])
    Destination = np.float32([[100,0], [280,0], [100,240], [280,240]])

    pts = np.array([[40, 145],[590, 145],[620, 300],[10, 300]], np.int32)
    pts = pts.reshape((-1,1,2))
    cv2.polylines(frame, [pts],True, (255, 0, 0), 3) 

    cv2.imshow("frame",frame)

    # time.sleep(10)
    
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break


cap.release()
cv2.destroyAllWindows()
exit()