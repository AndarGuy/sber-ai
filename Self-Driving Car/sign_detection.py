import cv2
import numpy as np

import color_utills as cu


# Функция детектирует совпадают ли цвета знака с предсказанным
def colors_match(img, predicted):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    col_tmp = set()
    for color in colors.keys():
        mask = cv2.inRange(hsv, np.array(colors[color][0]), np.array(colors[color][1]))
        if len(np.where(mask == 255)[0]) > 50:
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


# Изменяет изображение по заданным параметрам (возвращает измененное изображение)
def standartize_image(image):
    image = cv2.resize(image, (64, 64))
    # image = cv2.cvtColor(image, method)
    return image


# Возвращает словарь {имя знака: совпадение в процентах}
def get_matches(img, possible_signs):
    return {tpl: cv2.matchTemplate(standartize_image(img), standartize_image(templates[tpl]), cv2.TM_CCOEFF_NORMED) for
            tpl in
            possible_signs}


# возвращает массив с пороговой точностью
def drop_accuracy(arr, accuracy):
    return [a for a in arr.items if a[1] > accuracy]


# возвращает фигуру контура
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
STR_COLOR_YELLOW = 'yellow'
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
PEDESTRIAN_CROSSING = 'pedestrian_crossing'

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
        ACCOMPANYING_PRIORITY: {FORM: TAG_RECTANGLE, COLOR: [STR_COLOR_RED, STR_COLOR_BLUE]},
        PEDESTRIAN_CROSSING: {FORM: TAG_RECTANGLE, COLOR: [STR_COLOR_BLUE]}}

names_signs = [STOP, PEDESTRIAN_CROSSING, LEFT, RIGHT, FORWARD, BAD_ROAD, ONCOMING_PRIORITY, ACCOMPANYING_PRIORITY]
name_colors = [STR_COLOR_RED, STR_COLOR_BLUE]

# Инициализация cv темплейтов из файлов
templates = {name: standartize_image(cv2.imread(get_path(name))) for name in names_signs}

# Указываем цветовые диапазоны для знаков
colors = {STR_COLOR_RED: cu.get_color(STR_COLOR_RED), STR_COLOR_BLUE: cu.get_color(STR_COLOR_BLUE)}

# Красный
# Синий
# Черный
# colors[STR_COLOR_BLACK] = cu.get_color(STR_COLOR_BLUE)
# Белый
# colors[STR_COLOR_WHITE] = cu.get_color(STR_COLOR_BLUE)

# Создаем массив цветов дорожных знаков

MIN_ACCURACY = 0.3
PERFECT_ACCURACY = 0.6  # такая точность, при которой можно сказать, что это точно знак (игнорируется форма!)
MIN_CONTOUR_AREA = 6000


def get_sign(frame, possible_signs):
    # log = np.array(frame)
    # cont = np.array(frame)
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = np.array(frame)
    # blur = cv2.GaussianBlur(blur, (3, 3), 0)
    # blur = cv2.bilateralFilter(blur, 9, 120, 120)
    #cv2.imshow('frame', blur)
    hvs = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)

    for color in [STR_COLOR_RED, STR_COLOR_BLUE]:

        mask_def = cv2.inRange(hvs, np.array(colors[color][0]), np.array(colors[color][1]))
        mask_adv = np.array(mask_def)
        mask_adv = cv2.dilate(mask_adv, None, iterations=8)
        masks = [mask_adv, mask_def]

        for mask in masks:
            ret, thresh = cv2.threshold(mask, 127, 255, cv2.THRESH_TOZERO)
            _, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = [contour for contour in contours if cv2.contourArea(contour) > MIN_CONTOUR_AREA]
            hull = [cv2.convexHull(contours[i], False) for i in range(len(contours))]

            for e in hull:
                x, y, w, h = cv2.boundingRect(e)
                crop = frame[y:y + h, x:x + w]
                out = standartize_image(crop)
                matches = get_matches(out, possible_signs)
                matches = [m for m in matches.items() if m[1] > MIN_ACCURACY if
                           get_shape(e) == tags[m[0]][FORM] or m[1] > PERFECT_ACCURACY]
                if matches:
                    return max(matches, key=lambda x: x[1])[0]

    return None
