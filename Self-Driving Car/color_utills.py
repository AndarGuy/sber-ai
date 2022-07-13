def get_path(color):
    return './colors/{}.txt'.format(color)


def get_color(color):
    path = get_path(color)
    open(path, 'a').close()
    file = open(path, 'r+')
    return [[int(i) for i in line.split(': ')[1].split(', ')] for line in file.readlines()]
