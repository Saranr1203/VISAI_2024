import cv2
import time
from picamera2 import Picamera2

def cv():
    piCam = Picamera2()
    piCam.preview_configuration.main.size = (480,360)
    piCam.preview_configuration.main.format = "RGB888"
    piCam.preview_configuration.align()
    piCam.start()
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    blink_duration = 0
    eyes_open = True

    while(True):
        # Capture frame-by-frame
        frame = piCam.capture_array()
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frame[y:y+h, x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_gray)
            if(len(eyes)==0):
                if eyes_open:
                    blink_start_time = time.time()
                    eyes_open = False
                else:
                    blink_duration = time.time() - blink_start_time
                    print("Human Detected..!!")
            else:
                if not eyes_open:
                    blink_duration = time.time() - blink_start_time
                    if blink_duration > 0.5:  # Adjust this threshold as needed
                        print("Human Detected..!!")

                eyes_open = True
                
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cv2.destroyAllWindows()

