import RPi.GPIO as GPIO
import time
import cv2

GPIO.setwarnings(False)

EchoPin = 18
TrigPin = 16

#Set GPIO port to BCM coding mode
GPIO.setmode(GPIO.BOARD)

GPIO.setup(EchoPin,GPIO.IN)
GPIO.setup(TrigPin,GPIO.OUT)

#Ultrasonic function
def Distance():
    GPIO.output(TrigPin,GPIO.LOW)
    time.sleep(0.000002)
    GPIO.output(TrigPin,GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TrigPin,GPIO.LOW)

    t3 = time.time()

    while not GPIO.input(EchoPin):
        t4 = time.time()
        if (t4 - t3) > 0.03 :
            return -1
    t1 = time.time()
    while GPIO.input(EchoPin):
        t5 = time.time()
        if(t5 - t1) > 0.03 :
            return -1

    t2 = time.time()
    time.sleep(0.01)
    #print ("distance_1 is %d " % (((t2 - t1)* 340 / 2) * 100))
    return ((t2 - t1)* 340 / 2) * 100

count = 0

def Distance_test():
    num = 0
    ultrasonic = []
    while num < 5:
            distance = Distance()
            #print("distance is %f"%(distance) )
            while int(distance) == -1 :
                distance = Distance()
                #print("Tdistance is %f"%(distance) )
            while (int(distance) >= 500 or int(distance) == 0) :
                distance = Distance()
                #print("Edistance is %f"%(distance) )
            ultrasonic.append(distance)
            num = num + 1
            time.sleep(0.01)
    distance = (ultrasonic[1] + ultrasonic[2] + ultrasonic[3])/3
    print("count({}/20)".format(count), "distance is %f"%(distance) ) 
    return distance



while count < 20:
    distance = Distance_test()
    k= cv2.waitKey(30) & 0xff
    if k == 27:
        print ("27")
        break

    time.sleep(0.2)
    count += 1 



print("Ending")
GPIO.cleanup()

cv2.destroyAllWindows()
exit() 