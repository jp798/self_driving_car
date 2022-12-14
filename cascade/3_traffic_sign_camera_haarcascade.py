import cv2
import numpy as np
import time 


cap = cv2.VideoCapture(0)
cap.set(3,320) # set Width
cap.set(4,240) # set Height

# cap.set(cv2.CAP_PROP_EXPOSURE,-20.0)

cap.set(cv2.CAP_PROP_BRIGHTNESS,70)
cap.set(cv2.CAP_PROP_CONTRAST,70)
cap.set(cv2.CAP_PROP_SATURATION,70)
cap.set(cv2.CAP_PROP_GAIN,80)


traffic_cascade_name = '/home/pi/Desktop/self_driving_car-main/cascade/3_traffic_sign_cascade.xml'
traffic_cascade = cv2.CascadeClassifier()



#-- 1. Load the cascades
if not traffic_cascade.load(cv2.samples.findFile(traffic_cascade_name)):
    print('--(!)Error loading traffic_cascade cascade')
    exit(0)    

count = 0 


def traffic_sign(frame) :  

    try :

        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        cv2.imshow("frmae",frame)
        cv2.imshow("gary img",gray)


        img = None; 

        traffic_sign = traffic_cascade.detectMultiScale(gray)
        (x,y,w,h) = traffic_sign[0]

        return (True,(x,y,w,h))

    except : 

        return (False,())


def hsv_color_detection (limited_frame_copy) : 

    hsv = cv2.cvtColor(limited_frame_copy, cv2.COLOR_BGR2HSV)
    hue,_,_ = cv2.split(hsv)
    mean_of_hue = cv2.mean(hue)[0]
    # print(mean_of_hue)

    # hue = cv2.inRange(hue,3, 10)  ###### orange Mask     
    # hue = cv2.inRange(hue,70, 80)  ###### green Mask     
    hue = cv2.inRange(hue, 160, 180)  ###### Red Mask
    orange = cv2.bitwise_and(hsv, hsv, mask = hue)
    orange = cv2.cvtColor(orange, cv2.COLOR_HSV2BGR)

    cv2.imshow("3red_frame",orange)
    mean_of_hue = cv2.mean(hue)[0]

    return mean_of_hue




while True : 

    
    ret, frame  = cap.read()
    traffic_sign_result = traffic_sign(frame)


    if traffic_sign_result[0] : 

        (x,y,w,h) = traffic_sign_result[1]
        
        for (x,y,w,h) in traffic_sign:
            center = (x + w//2, y + h//2)
            img = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

        cv2.putText(img,"Red Traffic Sign", (x-30,y+20), cv2.FONT_HERSHEY_SIMPLEX,0.6,(255,255,0))
        cv2.imshow("test",img)
        

    else : 
        cv2.imshow("test",frame)

    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break

    time.sleep(0.1)

    