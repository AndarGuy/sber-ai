import cv2
import numpy as np

import color_utills as cu

WHITE = 'white_traffic'
BLACK = 'black_traffic'

BLACK_COLOR = cu.get_color(BLACK)
WHITE_COLOR = cu.get_color(WHITE)

MIN_CONTOUR_AREA = 200
MAX_CONTOUR_AREA = 6000
TARGET_LIGHT_AREA = 100

def is_rectangle(c):
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)

    if len(approx) == 4:
        return True
    else:
		return False

"""
def get_traffic_light(frame):
    colors_area = {
        color: len(np.where(cv2.inRange(frame, np.array(colors[color][0]), np.array(colors[color][1])) == 255)[0])
        for color in colors.keys()}
    return colors_area
"""

def get_traffic_light(frame):
	mask = cv2.inRange(frame, np.array(BLACK_COLOR[0]), np.array(BLACK_COLOR[1]))
	ret, thresh = cv2.threshold(mask, 127, 255, cv2.THRESH_TOZERO)
	_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	contours = [contour for contour in contours if MAX_CONTOUR_AREA > cv2.contourArea(contour) > MIN_CONTOUR_AREA if is_rectangle(contour)]
	for c in contours:
		x, y, w, h = cv2.boundingRect(e)
        crop = frame[y:y + h, x:x + w]
		red_area, amber_area, green_area = crop[0:h // 3, 0:w], crop[h // 3:h // 3 * 2, 0:w], crop[h // 3 * 2:h, 0:w]
		areas = {'red': red_area, 'amber': amber_area, 'green': green_area}
		detected_colors = []
		for area in areas:
			if len(cv2.inRange(areas[area], np.array(WHITE_COLOR[0]), np.array(WHITE_COLOR[1]))) > 100:
				detected_colors.append(area)
		
		if detected_colors:
			return detected_colors
			
	return []
				