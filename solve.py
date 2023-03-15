import time

import cv2 as cv
from PIL import Image, ImageGrab
import numpy

pic_name = ".md-pictures/README/image-20230314094817514.png"

points = []  # 有序点列表

# 依次是最左点横坐标,最下点纵坐标,最右点横坐标,最上点纵坐标
##
abs_left_x, abs_down_y, abs_right_x, abs_up_y = 106.521129, 29.565775, 106.545631, 29.587638
img = ""


def draw_point(_img, pos, color=(0, 0, 255), size=2):
    cv.circle(_img, pos, size, color, -1)


def calibration(_points):  # 校准
    rel_up_y = False
    for _i in _points:
        if (not rel_up_y) or rel_up_y >= _i[1]:
            rel_up_y = _i[1]
    rel_down_y = False
    for _i in _points:
        if (not rel_down_y) or rel_down_y <= _i[1]:
            rel_down_y = _i[1]
    rel_left_x = False
    for _i in _points:
        if (not rel_left_x) or rel_left_x >= _i[0]:
            rel_left_x = _i[0]

    rel_right_x = False
    for _i in _points:
        if (not rel_right_x) or rel_right_x <= _i[0]:
            rel_right_x = _i[0]

    _rate_y = (abs_up_y - abs_down_y) / (rel_down_y - rel_up_y)
    _rate_x = (abs_right_x - abs_left_x) / (rel_right_x - rel_left_x)
    print(_rate_y,_rate_x)
    return _rate_x, _rate_y, rel_left_x, rel_down_y


def re_draw():  # 重新画图
    img_to_show = img.copy()
    for _i in points:
        draw_point(img_to_show, _i, size=3)
    cv.namedWindow('image')
    cv.setMouseCallback('image', points_callback)
    cv.imshow('image', img_to_show)


def points_callback(event, x, y, flags, param):
    global down_flag, mode, points
    if event == cv.EVENT_RBUTTONDOWN:  # 右键删除上一个添加的点
        if not len(points) == 0:
            points.pop(len(points) - 1)
            re_draw()

    if event == cv.EVENT_LBUTTONDOWN:  # 增加模式
        points.append((x, y))
        re_draw()


# 106.533842,29.587713,106.533152,29.565797
def coordinate_trans(rel_pos, rel_left, rel_down, abs_left, abs_down, _rate_x, _rate_y):
    res = ((rel_pos[0] - rel_left) * _rate_x + abs_left, (rel_down-rel_pos[1]) * _rate_y + abs_down)
    return res


# 大渡口,江北termios

def solve():
    global img
    img = ImageGrab.grabclipboard()
    img = cv.cvtColor(numpy.asarray(img), cv.COLOR_RGB2BGR)
    re_draw()
    if cv.waitKey(0) & 0xFF == 27:
        cv.destroyAllWindows()

    rate_x, rate_y, rel_left_x, rel_down_y = calibration(points)

    abs_points = [coordinate_trans(i, rel_left_x, rel_down_y, abs_left_x, abs_down_y, rate_x, rate_y) for i in points]
    points.clear()
    return abs_points


res = solve()
for i in res:
    print(str(i[0]) + "," + str(i[1]))

print("------------------")
time.sleep(1)
