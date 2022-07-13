def write_color(hsv, path):
    open(path, 'a').close()
    file = open(path, 'w+')
    lowH, lowS, lowV = hsv[0]
    upH, upS, upV = hsv[1]
    file.writelines(['lowHSV: {0}, {1}, {2}\nupHSV: {3}, {4}, {5}'.format(lowH, lowS, lowV, upH, upS, upV)])
    file.close()


def get_color(path):
    open(path, 'a').close()
    file = open(path, 'r+')
    return [[int(i) for i in line.split(': ')[1].split(', ')] for line in file.readlines()]