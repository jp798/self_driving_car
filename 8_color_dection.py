import cv2
import time
import numpy as np 
import random


cap = cv2.VideoCapture(0)
cap.set(3,320) ### set Width 
cap.set(4,240) ### set Height


while True : 

    try : 
        ret , frame = cap.read()
        frame_copy = frame.copy()

        min_x = 200 
        max_x = 320 

        min_y = 20
        max_y = 100
        

        limited_polylines_list = [[min_x, max_y],  [max_x,max_y], [max_x, min_y], [min_x, min_y]]
        limited_polylines_list_1 = [[min_x-2, max_y+2],  [max_x+2, max_y+2], [max_x+2, min_y-2], [min_x-2, min_y-2]]


        pts = np.array(limited_polylines_list_1, np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(frame_copy, [pts],True, (0, 255, 0), 2) 

        cv2.imshow("frame",frame_copy)

        

        # shape_list = list(frame[10:310,10:80])
        # print(shape_list)

        matSrc = np.float32(limited_polylines_list)
        matDst = np.float32([[0,240], [320,240], [320,0], [0,0]])
        matAffine = cv2.getPerspectiveTransform(matSrc,matDst)# mat 1 src 2 dst
        limited_frame = cv2.warpPerspective(frame,matAffine,(320,240))

        cv2.imshow("limited_frame",limited_frame)
        

        hsv = cv2.cvtColor(limited_frame, cv2.COLOR_BGR2HSV)
        hue,_,_ = cv2.split(hsv)
        mean_of_hue = cv2.mean(hue)[0]
        print('color:',mean_of_hue)
        
        # hue = cv2.inRange(hue,24, 40)  ###### yellow Mask     
        # hue = cv2.inRange(hue,55, 75)  ###### green Mask     
        hue = cv2.inRange(hue, 160, 180)  ###### Red Mask
        orange = cv2.bitwise_and(hsv, hsv, mask = hue)
        orange = cv2.cvtColor(orange, cv2.COLOR_HSV2BGR)

        cv2.imshow("orange_frame",orange)
        # hue = np.delete(hue,0)
       

        mean_of_hue = cv2.mean(hue)[0]
       

        # if mean_of_hue > 65 and mean_of_hue < 80 : 
        #      print ("Green")

        # if mean_of_hue > 160 and mean_of_hue < 180 : 
        #      print ("Red")
        # cv2.waitKey()

        if mean_of_hue > 10 : 
            print ("Red:",mean_of_hue)

        else : 
            print (mean_of_hue)
        

        

        k = cv2.waitKey(30) & 0xff
        if k == 27 : ##### ESC 
            break 

        time.sleep(0.1)

    except Exception as E : 
        
        print("error->",E)

        cap.release()
        cv2.destroyAllWindows()
        exit()




cap.release()
cv2.destroyAllWindows()
exit()
