import cv2

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    cv2.putText(frame, "CERE", (10, 200), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5, cv2.LINE_8)
    cv2.circle(frame, (100, 100), 10, )



    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()