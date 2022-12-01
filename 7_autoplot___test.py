import cv2
import time
import enum
import numpy as np 
import YB_Pcb_Car  #Import Yahboom car library
import random

cap = cv2.VideoCapture(0)
cap.set(3,320) # set Width
cap.set(4,240) # set Height

cap.set(cv2.CAP_PROP_BRIGHTNESS,40)
cap.set(cv2.CAP_PROP_CONTRAST,40)
cap.set(cv2.CAP_PROP_SATURATION,20)
cap.set(cv2.CAP_PROP_GAIN,20)


car = YB_Pcb_Car.YB_Pcb_Car()
MOTOR_UP_SPEED = 70  ####   65 0 ~ 125 Speed 
MOTOR_DOWN_SPEED = 35   ####  30 

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
car.Ctrl_Servo(1, 90) #The servo connected to the S1 interface on the expansion board, rotate to 90°
time.sleep(0.5)
        
car.Ctrl_Servo(2, 135) #The servo connected to the S2 interface on the expansion board, rotate to 90°
time.sleep(0.5)



while True : 

    ret, frame = cap.read()





    ####### polylines ###########

    limited_polylines_list = [[10, 80],  [310, 80], [310, 10], [10, 10]]
    limited_polylines_list_1 = [[8, 82],  [312, 82], [312, 8], [8, 8]]
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
   

    left = np.sum(histogram[:int(histogram_length/4)])
    right = np.sum(histogram[int(3*histogram_length/4):])
    
    up = np.sum(histogram[int(2*histogram_length/4):int(3*histogram_length/4)])
    
    print("#####################")
    print("histogram",histogram)
    print ("{}|--({})--|{} ".format(left,right-left,right))

    if ( abs(right-left) > 100000) : 

        if right > left :  ### right 방향일 경우에... 
            direction = "RIGHT"
            print ("                   [[ RIGHT ]]:" ,right-left)
            Left()
        
        else :  #### Left 방향일 경우에 
            direction = "LEFT"
            print ("[[ LEFT ]]:", right-left)
            Right()


    else :  #### Up(직진) 방향일 경우에.... 
        print ("      [[ UP ]]:", up)

        if up < 10000 : #### up 가운데 부분을 분산도가 높지 않을 경우에... 

            Up() 
            
        else : 

            Up()
            ###### 수치 계산 따로 해야 함 
            # random_direction = random.randrange(1,7)
            # Down()
            # time.sleep(0.1)

            # if random_direction > 4 : 
            # car.Car_Spin_Left(40, 40)
            # else :
            #     car.Car_Spin_Right(40, 40)
            # time.sleep(0.1)
            car.Car_Stop()
            


    print(" #####################")


    # midpoint = np.int(histogram.shape[0]/2) 

    # time.sleep(1)
    
    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break


car.Car_Stop()
cap.release()
cv2.destroyAllWindows()
exit()
