import cv2
import time

import road_detection
import sign_detection
import traffic_light_detection

port = 'COM3'

cap = cv2.VideoCapture(1)

class Per:
    def __init__()

while True:

    ret, frame = cap.read()
    frame = cv2.resize(frame, (480, 360))

    detected_sign = sign_detection.get_sign(frame[0:240, 180:360])

    print(detected_sign)

    cv2.imshow('frame', frame[0:240, 180:360])

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
