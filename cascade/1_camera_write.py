import numpy as np
import cv2
import os,time



# Init camera 
cap = cv2.VideoCapture(0)
cap.set(3,320) # set Width
cap.set(4,240) # set Height

# cap.set(cv2.CAP_PROP_EXPOSURE,-20.0)

cap.set(cv2.CAP_PROP_BRIGHTNESS,70)
cap.set(cv2.CAP_PROP_CONTRAST,70)
cap.set(cv2.CAP_PROP_SATURATION,70)
cap.set(cv2.CAP_PROP_GAIN,80)





if True:
    t_start = time.time()
    fps = 0
    count = 0 
    
    while True:
        ret, frame = cap.read()

        tm_hour = time.gmtime(time.time() ).tm_hour
        tm_min = time.gmtime(time.time() ).tm_min
        tm_sec = time.gmtime(time.time() ).tm_sec
#         frame = cv2.flip(frame, -1) # Flip camera vertically
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # canny = cv2.Canny(frame,50,150)
        
        fps = fps + 1
        mfps = fps / (time.time() - t_start)
        #cv2.putText(frame, "FPS " + str(int(mfps)), (20,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
        #cv2.putText(frame,"Time "+ str(tm_hour) + ":"+str(tm_min) + ":"+ str(tm_sec) ,(20,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
        #cv2.putText(frame,"Frame "+ str(count) ,(20,60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)
        cv2.imshow('frame', frame)
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        
        
        cv2.imshow('gray_frame', gray_frame)
        # cv2.imshow('Canny', canny)
        
        
        k = cv2.waitKey(30) & 0xff
        if k == 27: # press 'ESC' to quit
            break
        
        if k == ord('s') : 

            # path = "./negative/traffic_sign"
            path = "./positive/traffic_sign"
            
            print("image:{}_{}.jpg saved".format(path,str(count)))
            cv2.imshow("{}_{}.jpg".format(path,str(count)),gray_frame)
            cv2.imwrite("{}_{}.jpg".format(path,str(count)),gray_frame)
            count += 1 

        time.sleep(0.2)
    


    cap.release()
    cv2.destroyAllWindows()
    exit()
