import uuid
import cv2
import numpy as np
from colorthief import ColorThief

cap = cv2.VideoCapture(0)


def colors_match(img, predicted):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    col_tmp = set()
    for color in colors.keys():
        mask = cv2.inRange(hsv, np.array(colors[color][0]), np.array(colors[color][1]))
        if len(np.where(mask == 255)[0]) > 100:
            col_tmp.add(color)
    if STR_COLOR_BLACK in tags[predicted[0]][COLOR] and STR_COLOR_BLUE in col_tmp:
        col_tmp.remove(STR_COLOR_BLUE)
    return set(tags[predicted[0]][COLOR]) == col_tmp


# Генератор пути до файла
def get_path(name):
    return PATH_TO_IMG + name + IMG_EXTENSION


# Переводим цвет из RGB в HSV
def to_hsv(rgb):
    return cv2.cvtColor(np.uint8([[rgb]]), cv2.COLOR_RGB2HSV)


# Берем основной цвет изображения, короме черного и белого
def get_dominant_color(path):
    color_thief = ColorThief(path)
    for color in color_thief.get_palette():
        if len(set([element > 20 for element in color])) > 1 or [element > 20 for element in color][0]:
            return color


def standartize_image(image):
    image = cv2.resize(image, (128, 128))
    # image = cv2.cvtColor(image, method)
    return image


def get_matches(img):
    return {tpl: cv2.matchTemplate(standartize_image(img), templates[tpl], cv2.TM_CCOEFF_NORMED) for tpl in
            templates.keys()}


def drop_accuracy(arr, accuracy):
    return [a for a in arr.items if a[1] > accuracy]


def get_shape(c):
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, 0.04 * peri, True)

    if len(approx) == 3:
        shape = "triangle"
    elif len(approx) == 4:
        shape = "rectangle"
    else:
        shape = "circle"
    return shape


STR_COLOR_BLACK = 'black'
STR_COLOR_GREEN = 'green'
STR_COLOR_RED = 'red'
STR_COLOR_WHITE = 'white'
STR_COLOR_BLUE = 'blue'
STR_COLOR_BACKGROUND = 'background'

COLORS = [STR_COLOR_BLACK, STR_COLOR_GREEN, STR_COLOR_RED, STR_COLOR_WHITE, STR_COLOR_BLUE]

COLOR_BLACK = (0, 0, 0)
COLOR_GREEN = (0, 255, 0)

FILE_SIZE = '1x'  # размер изображения(можно оставить путым)
PATH_TO_IMG = './img/' + FILE_SIZE + '/'  # путь до папки с изображением
IMG_EXTENSION = '.png'  # расширение файла

# Указание названий
STOP = 'stop'
LEFT = 'left'
RIGHT = 'right'
FORWARD = 'forward'
BAD_ROAD = 'bad_road'
ONCOMING_PRIORITY = 'oncoming_priority'
ACCOMPANYING_PRIORITY = 'accompanying_priority'

FORM = 'form'
COLOR = 'color'

TAG_CIRCLE = 'circle'
TAG_RECTANGLE = 'rectangle'
TAG_TRIANGLE = 'triangle'

tags = {STOP: {FORM: TAG_CIRCLE, COLOR: [STR_COLOR_RED]},
        LEFT: {FORM: TAG_CIRCLE, COLOR: [STR_COLOR_BLUE]},
        RIGHT: {FORM: TAG_CIRCLE, COLOR: [STR_COLOR_BLUE]},
        FORWARD: {FORM: TAG_CIRCLE, COLOR: [STR_COLOR_BLUE]},
        BAD_ROAD: {FORM: [TAG_TRIANGLE, TAG_RECTANGLE], COLOR: [STR_COLOR_RED]},
        ONCOMING_PRIORITY: {FORM: TAG_CIRCLE, COLOR: [STR_COLOR_RED]},
        ACCOMPANYING_PRIORITY: {FORM: TAG_RECTANGLE, COLOR: [STR_COLOR_RED, STR_COLOR_BLUE]}}

names_signs = [STOP, LEFT, RIGHT, FORWARD, BAD_ROAD, ONCOMING_PRIORITY, ACCOMPANYING_PRIORITY]
name_colors = [STR_COLOR_BLACK, COLOR_GREEN, STR_COLOR_RED, STR_COLOR_WHITE, STR_COLOR_BLUE]

# Инициализация cv темплейтов из файлов
templates = {name: standartize_image(cv2.imread(get_path(name))) for name in names_signs}

# Указываем цветовые диапазоны для знаков
colors = {}

# Красный
upHSV = [211, 193, 169]
lowHSV = [151, 69, 97]
colors[STR_COLOR_RED] = (lowHSV, upHSV)
# Синий
upHSV = [148, 239, 227]
lowHSV = [87, 97, 108]
colors[STR_COLOR_BLUE] = (lowHSV, upHSV)
# Черный
upHSV = [157, 120, 53]
lowHSV = [0, 10, 12]
# colors[STR_COLOR_BLACK] = (lowHSV, upHSV)
# Белый
upHSV = [147, 63, 255]
lowHSV = [84, 3, 173]
# colors[STR_COLOR_WHITE] = (lowHSV, upHSV)

# Создаем массив цветов дорожных знаков

MIN_ACCURACY = 0.4

while True:

    ret, frame = cap.read()
    frame = cv2.resize(frame, (np.array(frame).shape[1] // 3, np.array(frame).shape[0] // 3))
    log = np.array(frame)
    cont = np.array(frame)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = np.array(frame)
    # blur = cv2.GaussianBlur(blur, (5, 5), 0)
    blur = cv2.bilateralFilter(blur, 9, 120, 120)
    hvs = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    potentialSigns = []

    for color in [STR_COLOR_BLUE, STR_COLOR_RED]:

        mask_def = cv2.inRange(hvs, np.array(colors[color][0]), np.array(colors[color][1]))
        mask_adv = np.array(mask_def)
        mask_adv = cv2.dilate(mask_adv, None, iterations=8)
        masks = [mask_adv, mask_def]

        cv2.imshow('mask ' + color, mask_adv)

        for mask in masks:
            ret, thresh = cv2.threshold(mask, 127, 255, cv2.THRESH_TOZERO)
            contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = [contour for contour in contours if cv2.contourArea(contour) > 400]
            hull = [cv2.convexHull(contours[i], False) for i in range(len(contours))]

            cv2.drawContours(cont, hull, -1, tuple(np.mean([colors[color][0], colors[color][1]], axis=0)), -1)

            for e in hull:
                x, y, w, h = cv2.boundingRect(e)
                crop = frame[y:y + h, x:x + w]
                out = standartize_image(crop)
                matches = get_matches(out)
                matches = [m for m in matches.items() if m[1] > MIN_ACCURACY if colors_match(out, m) if
                           get_shape(e) == tags[m[0]][FORM] or m[1] > 0.55]
                if matches:
                    cv2.imshow('out', out)
                    print('time:', uuid.uuid4().__str__(), 'I really think that is a', max(matches, key=lambda x: x[1])[0], 'with shape', get_shape(e))

    color = COLOR_BLACK

    # cv2.putText(frame, str(winner), (5, 30), cv2.QT_FONT_NORMAL, 1, color, 1, cv2.LINE_8)
    # cv2.imshow('temp', templates[winner[0]])
    cv2.imshow('frame', frame)
    cv2.imshow('log', log)
    cv2.imshow('contour', cont)
    cv2.imshow('blur', blur)
    # cv2.imshow('blur', blur)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
