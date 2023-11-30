import RPi.GPIO as GPIO
import time
import cv2

def setup_gpio(echo_pin, trig_pin):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(echo_pin, GPIO.IN)
    GPIO.setup(trig_pin, GPIO.OUT)

def get_distance(trig_pin, echo_pin, timeout=0.03):
    # Send trigger signal
    GPIO.output(trig_pin, GPIO.LOW)
    time.sleep(0.000002)
    GPIO.output(trig_pin, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(trig_pin, GPIO.LOW)

    start_time = time.time()

    # Wait for echo start
    while not GPIO.input(echo_pin):
        if time.time() - start_time > timeout:
            return -1

    echo_start = time.time()

    # Wait for echo end
    while GPIO.input(echo_pin):
        if time.time() - echo_start > timeout:
            return -1

    echo_end = time.time()
    return ((echo_end - echo_start) * 340 / 2) * 100

def get_average_distance(trig_pin, echo_pin, samples=5):
    distances = []
    for _ in range(samples):
        distance = get_distance(trig_pin, echo_pin)
        if distance != -1 and 0 < distance < 500:
            distances.append(distance)
        time.sleep(0.01)

    if len(distances) > 0:
        return sum(distances) / len(distances)
    else:
        return -1

def main():
    EchoPin = 18
    TrigPin = 16
    setup_gpio(EchoPin, TrigPin)

    for count in range(20):
        distance = get_average_distance(TrigPin, EchoPin)
        print(f"count({count+1}/20) - Distance: {distance:.2f} cm")

        if cv2.waitKey(30) & 0xff == 27:
            print("Esc key pressed. Exiting.")
            break

        time.sleep(0.2)

    print("Ending")
    GPIO.cleanup()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
