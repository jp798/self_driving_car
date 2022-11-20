import numpy as np
import cv2
import os,time



# Init camera 
cap = cv2.VideoCapture(0)
cap.set(3,320) # set Width
cap.set(4,240) # set Height



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
        gray_frame = cv2.add (gray_frame,-20)
        # dst_retval, dst_binaryzation = cv2.threshold(gray_frame, 10, 255, cv2.THRESH_BINARY)   #### 밝기부분
        cv2.imshow('frame', gray_frame)
        # cv2.imshow('Canny', canny)
        count += 1 
        k = cv2.waitKey(30) & 0xff
        if k == 27: # press 'ESC' to quit
            break
        
        if k == ord('s') : 
            print("image:",mfps,".jpg save")
            cv2.imshow("./image/{}.jpg".format(mfps),gray_frame)
            cv2.imwrite("./image/{}.jpg".format(mfps),gray_frame)


    cap.release()
    cv2.destroyAllWindows()
    exit()
