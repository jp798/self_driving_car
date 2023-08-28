import cv2

# Initialize the camera
cap = cv2.VideoCapture(0)

# Set camera width and height
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Display the frame
    cv2.imshow('Frame', frame)

    # Save the frame when 'a' is pressed
    if cv2.waitKey(1) & 0xFF == ord('a'):
        cv2.imwrite('captured_image.jpg', frame)
        print("Image saved!")


    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera
cap.release()
cv2.destroyAllWindows()
