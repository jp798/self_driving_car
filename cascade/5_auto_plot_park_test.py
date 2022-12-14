import cv2
import time
import enum
import numpy as np 
import YB_Pcb_Car  #Import Yahboom car library
import random

cap = cv2.VideoCapture(0)
cap.set(3,320) # set Width
cap.set(4,240) # set Height

cap.set(cv2.CAP_PROP_BRIGHTNESS,45)
cap.set(cv2.CAP_PROP_CONTRAST,90)
cap.set(cv2.CAP_PROP_SATURATION,20)
cap.set(cv2.CAP_PROP_GAIN,20)


car = YB_Pcb_Car.YB_Pcb_Car()
MOTOR_UP_SPEED = 150  ####   65 0 ~ 125 Speed 
MOTOR_DOWN_SPEED = 70   ####  30 

DETECT_VALUE = 30  #### 밝기 70 /130

IS_STOP = False 

def Up() : 
    car.Car_Run(MOTOR_UP_SPEED-35, MOTOR_UP_SPEED-35)
    time.sleep(0.1)
    
    if IS_STOP : 
        car.Car_Stop()

def Down() : 
    car.Car_Back(MOTOR_UP_SPEED-40, MOTOR_UP_SPEED-40)
    time.sleep(0.1)
    
    if IS_STOP : 
        car.Car_Stop()

def Left() : 
    car.Car_Left(MOTOR_DOWN_SPEED, MOTOR_UP_SPEED)
    # car.Car_Spin_Left(MOTOR_UP_SPEED, MOTOR_UP_SPEED)
    time.sleep(0.1)
    
    if IS_STOP : 
        car.Car_Stop()

def Right() : 
    car.Car_Right(MOTOR_UP_SPEED, MOTOR_DOWN_SPEED)
    # car.Car_Spin_Right(MOTOR_UP_SPEED, MOTOR_UP_SPEED)
    time.sleep(0.1)
    
    if IS_STOP : 
        car.Car_Stop()


    direction = None 
    count = 0 

#######  90° arc 
#car.Ctrl_Servo(1, 90) #The servo connected to the S1 interface on the expansion board, rotate to 90°
#time.sleep(0.5)
        
#car.Ctrl_Servo(2, 135) #The servo connected to the S2 interface on the expansion board, rotate to 90°
#time.sleep(0.5)




def isParkSign(frame) : 

    try : 
        
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        traffic_cascade_name = 'cascade.xml'
        traffic_cascade = cv2.CascadeClassifier()

        if not traffic_cascade.load(cv2.samples.findFile(traffic_cascade_name)):
            print('--(!)Error loading traffic_cascade cascade')

        traffic_sign = traffic_cascade.detectMultiScale(gray)
        for (x,y,w,h) in traffic_sign:
            center = (x + w//2, y + h//2)
            img = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)

            print(traffic_sign)

        
        (x,y,w,h) = traffic_sign[0]

        cv2.putText(img,"Park OK(sign)", (x-20,y+h+10), cv2.FONT_HERSHEY_SIMPLEX,0.7,(255,255,255))
        cv2.imshow("0.Park OK(sign)",img)
    
        return { "success" :True, "rect": (x,y,w,h)}

    except : 
        
        # cv2.imshow("stop sign",frame)
        cv2.imshow("0.Park OK(sign)",frame)

        return {"success": False, "rect" : ()}

    




try : 

    while True : 

        ret, frame = cap.read()

        park_sign = isParkSign(frame.copy())

        if park_sign["success"] : 

            ##### 주차 시스템 동작 
            # Up()
            # time.sleep(0.5)
            # Right()
            # time.sleep(0.5)
            print("Park OK")

            car.Car_Stop()

        else :   

            ####### polylines ###########

            limited_polylines_list = [[10, 80],  [310, 80], [310, 10], [10, 10]]
            limited_polylines_list_1 = [[8, 100],  [312, 100], [312, 8], [8, 8]]
            pts = np.array(limited_polylines_list_1, np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(frame, [pts],True, (255, 0, 0), 2) 
            cv2.imshow("1_polylines",frame)
            


            matSrc = np.float32(limited_polylines_list)
            matDst = np.float32([[0,240], [320,240], [320,0], [0,0]])
            matAffine = cv2.getPerspectiveTransform(matSrc,matDst)# mat 1 src 2 dst
            limited_frame = cv2.warpPerspective(frame,matAffine,(320,240))

            cv2.imshow("2_limited_frame",limited_frame)




            #####  gray ############
            gray_frame = cv2.cvtColor(limited_frame, cv2.COLOR_RGB2GRAY)   
            # gray_frame = cv2.Canny(gray_frame,105,105)
            
            dst_retval, dst_binaryzation = cv2.threshold(gray_frame, DETECT_VALUE, 255, cv2.THRESH_BINARY)   #### 밝기부분
            dst_binaryzation = cv2.erode(dst_binaryzation, None, iterations=1)   






            cv2.imshow("3_gray_frame",gray_frame)
            cv2.imshow("4_dst_binaryzation",dst_binaryzation)
            print("dst_binaryzation",dst_binaryzation.shape)

            # histogram = list(np.sum(dst_binaryzation[dst_binaryzation.shape[0]//2:, :], axis=0)) 
            histogram = list(np.sum(dst_binaryzation[:, :], axis=0))   ##### 전체를 읽어서, 판단함.
            histogram_length = len(histogram)
        

            left = int(np.sum(histogram[:int(histogram_length/4)]))
            right = int(np.sum(histogram[int(3*histogram_length/4):]))
            
            up = np.sum(histogram[int(2*histogram_length/4):int(3*histogram_length/4)])
            
            print("#####################")
            print("histogram",histogram)
            print ("{}|--({})--|{} ".format(left,right-left,right))

            if ( abs(right-left) > 1000) : 

                if right > left :  ### right 방향일 경우에... 
                    direction = "RIGHT"
                    
                    print ("                   [[ RIGHT ]]:" ,right-left)
                    # Left()
                
                else :  #### Left 방향일 경우에 
                    direction = "LEFT"
                    print ("[[ LEFT ]]:", right-left)
                    # Right()


            else :  #### Up(직진) 방향일 경우에.... 
                print ("      [[ UP ]]:", up)

                if up < 10000 : 

                    # Up() 
                    pass
                    
                else : 
                    # Up()
                    pass
                    

            print(" #####################")


        # midpoint = np.int(histogram.shape[0]/2) 

        # time.sleep(1)
        # cv2.destroyAllWindows()
        
        k = cv2.waitKey(30) & 0xff
        if k == 27: # press 'ESC' to quit
            break


except Exception as E : 
    
    print("error->",E)

    car.Car_Stop()
    cap.release()
    cv2.destroyAllWindows()
    exit()


car.Car_Stop()
cap.release()
cv2.destroyAllWindows()
exit()
