import cv2
import numpy as np

window_name = "Window"

color = input('Введите цвет:' + '\n')
path = './colors/' + color + '.txt'


def callback(x):
    upH = cv2.getTrackbarPos("upH", window_name)
    upV = cv2.getTrackbarPos("upV", window_name)
    upS = cv2.getTrackbarPos("upS", window_name)
    lowH = cv2.getTrackbarPos("lowH", window_name)
    lowV = cv2.getTrackbarPos("lowV", window_name)
    lowS = cv2.getTrackbarPos("lowS", window_name)

    write_color([[lowH, lowS, lowV], [upH, upS, upV]])


def write_color(hsv):
    open(path, 'a').close()
    file = open(path, 'w+')
    lowH, lowS, lowV = hsv[0]
    upH, upS, upV = hsv[1]
    file.writelines(['lowHSV: {0}, {1}, {2}\nupHSV: {3}, {4}, {5}'.format(lowH, lowS, lowV, upH, upS, upV)])
    file.close()


def get_color():
    open(path, 'a').close()
    file = open(path, 'r+')
    return [[int(i) for i in line.split(': ')[1].split(', ')] for line in file.readlines()]


if not get_color():
    write_color([[0, 0, 0], [0, 0, 0]])
    lowH, lowS, lowV, upH, upS, upV = [0] * 6
else:
    hsv = get_color()
    lowH, lowS, lowV = hsv[0]
    upH, upS, upV = hsv[1]

print(get_color())

cv2.namedWindow(window_name)
cv2.createTrackbar("lowH", window_name, lowH, 255, callback)
cv2.createTrackbar("lowS", window_name, lowS, 255, callback)
cv2.createTrackbar("lowV", window_name, lowV, 255, callback)
cv2.createTrackbar("upH", window_name, upH, 255, callback)
cv2.createTrackbar("upS", window_name, upS, 255, callback)
cv2.createTrackbar("upV", window_name, upV, 255, callback)

frame = cv2.imread('./img/test/Picture110.jpg')

while True:
    hsv = get_color()

    lower = np.array(hsv[0])
    upper = np.array(hsv[1])

    hvs = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hvs, lower, upper)
    res = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cv2.destroyAllWindows()
