
import cv2
import time
import enum


import threading
import inspect
import ctypes
import matplotlib.pyplot as plt
import PID

def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)


import YB_Pcb_Car  #Import Yahboom library

car = YB_Pcb_Car.YB_Pcb_Car()
car.Ctrl_Servo(1,93)
car.Ctrl_Servo(2,160)



def bgr8_to_jpeg(value, quality=75):
    return bytes(cv2.imencode('.jpg', value)[1])

image = cv2.VideoCapture(0)
image.set(3,640)
image.set(4,480)
image.set(5, 30)  #set frame
# fourcc = cv2.VideoWriter_fourcc(*"MPEG")
image.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
image.set(cv2.CAP_PROP_BRIGHTNESS, 60) 
#image.set(cv2.CAP_PROP_CONTRAST, 50) 
#image.set(cv2.CAP_PROP_EXPOSURE, 156) 
#ret, frame = image.read()
#image_widget.value = bgr8_to_jpeg(frame)


global Z_axis_pid
Z_axis_pid = PID.PositionalPID(0.5, 0, 1)  #1.2 0 0.1   
global prev_left
prev_left = 0
global prev_right
prev_right = 0


def Camera_display():
    global peaks_count
    global prev_left, prev_right
    t_start = time.time()
    fps = 0
    global Z_axis_pid
    
    while 1:

        ret, frame = image.read()
        

        fps = fps + 1
        mfps = fps / (time.time() - t_start)
        cv2.putText(frame, "FPS: " + str(int(mfps)), (80,80), cv2.FONT_HERSHEY_SIMPLEX, 3.0, (0,255,255), 8)
        

        frame = cv2.resize(frame,(320,240))
        
        
        matSrc = np.float32([[0, 149],  [320, 149], [281, 72], [43, 72]])
        matDst = np.float32([[0,240], [320,240], [320,0], [0,0]])
        matAffine = cv2.getPerspectiveTransform(matSrc,matDst)# mat 1 src 2 dst
        dst = cv2.warpPerspective(frame,matAffine,(320,240))
        

        pts = np.array([[0, 149],  [320, 149], [281, 72], [43, 72]], np.int32)
      
        pts = pts.reshape((-1, 1, 2))
        cv2.polylines(frame, [pts],True, (255, 0, 0), 3) 

        dst_gray = cv2.cvtColor(dst, cv2.COLOR_RGB2GRAY)   
        dst_retval, dst_binaryzation = cv2.threshold(dst_gray, 120, 255, cv2.THRESH_BINARY)   
        dst_binaryzation = cv2.erode(dst_binaryzation, None, iterations=1)                
        
 
        histogram = np.sum(dst_binaryzation[dst_binaryzation.shape[0]//2:, :], axis=0)  
        midpoint = np.int(histogram.shape[0]/2) 
        
        left_sum = np.sum(histogram[:20], axis=0)  
        right_sum = np.sum(histogram[300:], axis=0)  
        
        #print("left_sum =%d "%left_sum)
        #print("right_sum = %d"%right_sum)
        
        
        rightpoint = 320
        center_r = 159
        #print (histogram)
        #print(histogram[::-1])
        #plt.plot(histogram)
        #plt.plot(histogram[::-1])
        #plt.show()

        leftx_base = np.argmin(histogram[:rightpoint], axis = 0)
        rightx_base = np.argmin(histogram[::-1][:rightpoint], axis = 0) 
        rightx_base = 319 - rightx_base

        dst_binaryzation = cv2.cvtColor(dst_binaryzation,cv2.COLOR_GRAY2RGB)
        cv2.line(dst_binaryzation,(159,0),(159,240),(255,0,255),2)  
        lane_center = int((leftx_base + rightx_base)/2)  
        #print("lane_center")
        #print(lane_center)
        cv2.line(dst_binaryzation,(leftx_base,0),(leftx_base,240),(0,255,0),2)   
        cv2.line(dst_binaryzation,(rightx_base,0),(rightx_base,240),(0,255,0),2) 
        cv2.line(dst_binaryzation,(lane_center,0),(lane_center,240),(255,0,0),2) 
        
        left_sum_value = int(np.sum(histogram[:center_r], axis = 0))/159
        right_sum_value = int(np.sum(histogram[center_r:], axis = 0))/159
        #print("left_sum_value = %d", left_sum_value)
        #print("right_sum_value = %d", right_sum_value)

        Bias = 159 - lane_center
        cv2.putText(dst_binaryzation, "FPS:  " + str(int(mfps)), (10,15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 1)
        cv2.putText(dst_binaryzation, "Bias: " + str(int(Bias)), (10,35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,255), 1)
        #print(Bias)
        

        Z_axis_pid.SystemOutput = Bias
        Z_axis_pid.SetStepSignal(0)
        Z_axis_pid.SetInertiaTime(0.5, 0.2)
        
        
        if Z_axis_pid.SystemOutput > 25: # 20
            Z_axis_pid.SystemOutput = 25
        elif Z_axis_pid.SystemOutput < -25:
            Z_axis_pid.SystemOutput = -25
            
        TurnZ_PID_slider.value = int(Z_axis_pid.SystemOutput)
        
       
        if leftx_base == 0 and rightx_base == 319:
            if prev_left > prev_right:
                car.Control_Car(-70, 60)
            elif prev_left < prev_right:
                car.Control_Car(70, -70)
                
            prev_left = 0
            prev_right = 0
            
        else:
            if Bias > 3:   
                #prev_left = 1
                #prev_right = 0
                if Bias > 140: 
                    car.Control_Car(-70, 60)
                    prev_left = 0
                    prev_right = 0
                else:
                    car.Control_Car(45+int(Z_axis_pid.SystemOutput), 45-int(Z_axis_pid.SystemOutput))
                time.sleep(0.001) 
            elif Bias < -3:    
                #prev_right = 1
                #prev_left = 0
                if Bias < -140:   
                    car.Control_Car(60, -70)
                    prev_left = 0
                    prev_right = 0
                else:
                    car.Control_Car(45+int(Z_axis_pid.SystemOutput), 45-int(Z_axis_pid.SystemOutput))
                time.sleep(0.001)

            else:
                car.Car_Run(45, 45)
     
        


        if left_sum != right_sum:
            if left_sum < right_sum:
                prev_left = prev_left + 1
            elif right_sum < left_sum:
                prev_right = prev_right + 1

        

        image_widget.value = bgr8_to_jpeg(frame)
        image_widget_1.value = bgr8_to_jpeg(dst)
        image_widget_2.value = bgr8_to_jpeg(dst_binaryzation)



thread3 = threading.Thread(target=Camera_display)
thread3.setDaemon(True)
thread3.start()


stop_thread(thread3)
car.Car_Stop()

image.release()