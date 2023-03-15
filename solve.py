import time

import cv2 as cv
from PIL import Image, ImageGrab
import numpy
import pyperclip

pic_name = ".md-pictures/README/image-20230314094817514.png"

points = []  # 有序点列表

clipboard_lastval=pyperclip.paste()
def clipboard_changed():
    contain = pyperclip.paste()
    global clipboard_lastval
    if not contain == clipboard_lastval:
        clipboard_lastval=contain
        return True
    return False
# 依次是最左点横坐标,最下点纵坐标,最右点横坐标,最上点纵坐标
##
inf=999999999

abs_left_x, abs_down_y, abs_right_x, abs_up_y =inf,inf,-inf,-inf
img = ""


def draw_point(_img, pos, color=(0, 0, 255), size=2):
    cv.circle(_img, pos, size, color, -1)
# 106.533221,29.56578
#

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
    re_draw()
    if cv.waitKey(0) & 0xFF == 27:
        cv.destroyAllWindows()

    rate_x, rate_y, rel_left_x, rel_down_y = calibration(points)

    abs_points = [coordinate_trans(i, rel_left_x, rel_down_y, abs_left_x, abs_down_y, rate_x, rate_y) for i in points]
    points.clear()
    return abs_points

while True:
    abs_left_x, abs_down_y, abs_right_x, abs_up_y =inf,inf,-inf,-inf
    i=0
    while i<4:
        time.sleep(0.5)
        if clipboard_changed():
            print("读取剪切板",clipboard_lastval)
            x,y=map(float,clipboard_lastval.split(","))
            abs_left_x=min(abs_left_x,x) 
            abs_right_x=max(abs_right_x,x)
            abs_down_y=min(abs_down_y,y)
            abs_up_y=max(abs_up_y,y)           
            i+=1

    while i <5:
        time.sleep(0.5)
        if clipboard_changed():
            print("读取图片")
            img = ImageGrab.grabclipboard()
            img = cv.cvtColor(numpy.asarray(img), cv.COLOR_RGB2BGR)
            i += 1
    res = solve()
    for i in res:
        print(str(i[0]) + "," + str(i[1]))

    print("------------------")
    time.sleep(1)
