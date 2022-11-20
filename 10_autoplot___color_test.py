import cv2
import time
import enum
import numpy as np 
import YB_Pcb_Car  #Import Yahboom car library
import random
import RPi.GPIO as GPIO

cap = cv2.VideoCapture(0)
cap.set(3,320) # set Width
cap.set(4,240) # set Height

car = YB_Pcb_Car.YB_Pcb_Car()
MOTOR_UP_SPEED = 75  ####   65 0 ~ 125 Speed 
MOTOR_DOWN_SPEED = 30   ####  30 

DETECT_VALUE = 110  #### 70 

IS_STOP = False 



##### Buzzer Setting 
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)

p = GPIO.PWM(32, 220) 

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
    car.Car_Left(MOTOR_DOWN_SPEED, MOTOR_UP_SPEED-5)
    # car.Car_Spin_Left(MOTOR_UP_SPEED, MOTOR_UP_SPEED)
    time.sleep(0.1)
    
    if IS_STOP : 
        car.Car_Stop()

def Right() : 
    car.Car_Right(MOTOR_UP_SPEED-5, MOTOR_DOWN_SPEED)
    # car.Car_Spin_Right(MOTOR_UP_SPEED, MOTOR_UP_SPEED)
    time.sleep(0.1)
    
    if IS_STOP : 
        car.Car_Stop()


    direction = None 
    count = 0 

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

    ######### limited frame (색깔 인식)
    limited_frame_copy = limited_frame.copy()

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


    if mean_of_hue > 10 : 
        p.start(20)
        car.Car_Stop()
        time.sleep(0.5)
        print ("Red:",mean_of_hue)
        p.stop()





    #####  gray ############
    gray_frame = cv2.cvtColor(limited_frame, cv2.COLOR_RGB2GRAY)   
    # gray_frame = cv2.Canny(gray_frame,105,105)
    
    dst_retval, dst_binaryzation = cv2.threshold(gray_frame, DETECT_VALUE, 255, cv2.THRESH_BINARY)   #### 밝기부분
    dst_binaryzation = cv2.erode(dst_binaryzation, None, iterations=1)   



    cv2.imshow("4_gray_frame",gray_frame)
    cv2.imshow("5_dst_binaryzation",dst_binaryzation)
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

        if up < 10000 : 

            Up() 
            # pass
        else : 

            random_direction = random.randrange(1,7)
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
