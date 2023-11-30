import numpy as np
import cv2
import time

def get_current_time():
    return time.gmtime(time.time())

def calculate_fps(start_time, frame_count):
    return frame_count / (time.time() - start_time)

cap = cv2.VideoCapture(0)
cap.set(3, 320)  # set Width
cap.set(4, 240)  # set Height

t_start = time.time()
fps = 0
count = 0

try:
    while True:
        ret, frame = cap.read()
        tm_hour, tm_min, tm_sec = get_current_time()[3:6]

        # frame = cv2.flip(frame, -1) # Flip camera vertically
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame = cv2.Canny(frame,50,150)


        mfps = calculate_fps(t_start, fps)
        cv2.putText(frame, f"FPS {int(mfps)}", (20, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(frame, f"Time {tm_hour}:{tm_min}:{tm_sec}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        cv2.putText(frame, f"Frame {count}", (20, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        cv2.imshow('frame', frame)
        count += 1
        fps += 1

        if cv2.waitKey(30) & 0xff == 27:  # press 'ESC' to quit
            break

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    cap.release()
    cv2.destroyAllWindows()
