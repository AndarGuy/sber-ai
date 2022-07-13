import cv2
import numpy as np
from colorthief import ColorThief


def getHSV(rgb):
    return cv2.cvtColor(np.uint8([[rgb]]), cv2.COLOR_RGB2HSV)


def getDominantColor(path):
    color_thief = ColorThief(path)
    for color in color_thief.get_palette():
        if len(set([element > 20 for element in color])) > 1 or [element > 20 for element in color][0]:
            return color


print(getDominantColor('./img/3x/bad_road.png'))
