import cv2
import numpy as np
import time 


cap = cv2.VideoCapture(0)
cap.set(3,320) # set Width
cap.set(4,240) # set Height

# cap.set(cv2.CAP_PROP_EXPOSURE,-20.0)

cap.set(cv2.CAP_PROP_BRIGHTNESS,30)
cap.set(cv2.CAP_PROP_CONTRAST,90)
cap.set(cv2.CAP_PROP_SATURATION,70)
cap.set(cv2.CAP_PROP_GAIN,80)


# traffic_cascade_name = '2_traffic_sign_red_cascade-org.xml'
traffic_cascade_name = 'cascade.xml'
traffic_cascade = cv2.CascadeClassifier()



#-- 1. Load the cascades
if not traffic_cascade.load(cv2.samples.findFile(traffic_cascade_name)):
    print('--(!)Error loading traffic_cascade cascade')
    exit(0)    

count = 0 


while True : 

    ###-- 2. 이미지 읽기 

    ret, frame  = cap.read()


    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    cv2.imshow("frmae",frame)
    cv2.imshow("gary img",gray)


    img = None; 

    traffic_sign = traffic_cascade.detectMultiScale(gray)
    for (x,y,w,h) in traffic_sign:
        center = (x + w//2, y + h//2)
        img = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

    print(traffic_sign)

   

    try : 
        (x,y,w,h) = traffic_sign[0]

        cv2.putText(img,"Park OK(sign)", (x-20,y-10), cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255))
        cv2.imshow("test",img)
        # cv2.imwrite("./test/test_{}.jpg".format(str(count)), img)

        count += 1 

    except : 
        cv2.imshow("test",frame)

    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break

    time.sleep(0.1)

    
