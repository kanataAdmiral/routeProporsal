import hashlib
import csv
import math
import sys

import numpy as np

from rection1.models import User

from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon, Feature

from rection1.exception import Exception
from scipy.spatial import distance

salt = bytes("b'pelob/9gQSxIsZ66wlu+wblqY8wuqT0HQl7TODMotyA='", 'utf-8')


def get_digest(password):
    password = bytes(password, 'utf-8')
    digest = hashlib.sha256(salt + password).hexdigest()
    for _ in range(10000):
        digest = hashlib.sha256(bytes(digest, 'utf-8')).hexdigest()
    return digest


def login_check(user_id, loginPass):
    loginPass = get_digest(loginPass)
    try:
        matchUser = User.objects.get(id=user_id)
        if matchUser.password == loginPass:
            return True
        else:
            raise Exception.LoginException('パスワードが違います')
    except User.DoesNotExist:
        raise Exception.LoginException('ユーザが見つかりません')


def is_position_inside_polygon(rowList, columnList, position) -> bool:
    points = []
    inside_poly = []

    # ポリゴンのポジション情報を取得
    for i in range(len(rowList)):
        points.append((columnList[i], rowList[i]))
    inside_poly.append(points)
    poly = Polygon(inside_poly)

    point = Feature(geometry=Point((position[0], position[1])))

    return boolean_point_in_polygon(point, poly)


def fill_paddy(paddyArray, row, column, string):
    row = math.floor(row)
    column = math.floor(column)
    # if string == pp.OUTSIDE_POSITION:
    #     print("paddy[", row, "][", column, "]が外周")
    # elif string == pp.INSIDE_POSITION:
    #     print("paddy[", row, "][", column, "]が内周")
    # elif string == pp.START_POSITION:
    #     print("paddy[", row, "][", column, "]が入口")
    # elif string == pp.END_POSITION:
    #     print("paddy[", row, "][", column, "]が出口")

    if paddyArray[row][column] == 0:
        paddyArray[row][column] = string
    else:
        print("paddyArray[", row, "][", column, "]is not void")


def fill_position(paddyArray, x, y, string, flag=True):
    if paddyArray[y][x] == 0:
        paddyArray[y][x] = string
    else:
        if flag:
            print("paddyArray is not void")
        else:
            paddyArray[y][x] = string


def fill_paddy_route(paddyArray, mp):
    x = mp.column_position
    y = mp.row_position
    try:
        if paddyArray[y][x] == 0:
            paddyArray[y][x] = fill_icon(mp.icon, mp.plant)
        else:
            paddyArray[y][x] = paddyArray[y][x] + fill_icon(mp.icon, mp.plant)
    except IndexError as e:
        print("アルゴルズムに内部的エラーが発生")
        sys.exit()


def fill_icon(icon, plant):
    if plant:
        return icon
    else:
        if icon == '↑':
            return '⇡'
        elif icon == '↓':
            return '⇣'
        elif icon == '→':
            return '⇢'
        elif icon == '←':
            return '⇠'


def export_to_file(any_list, fileName='paddyArray'):
    filePath = 'C:/Users/196009/Desktop/' + fileName + '.csv'
    print(filePath, "に書き込み中")
    with open(filePath, 'w', encoding='utf_8_sig') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(any_list)
    print(filePath, "に書き込み完了")


# 原点とする座標をx, yで渡す
# 動かしたい座標をuで渡す
# 最も高い点を中心に回転した後のx軸, y軸, z軸を返す
def rotation_o(u, t, x, y, deg=False):
    # 度数単位の角度をラジアンに変換
    if deg:
        t = np.deg2rad(t)

    # 回転行列
    # あふぃんへんかい
    R = np.array([[np.cos(t), -np.sin(t), -x * np.cos(t) + y * np.sin(t)],
                  [np.sin(t), np.cos(t), -x * np.sin(t) - y * np.cos(t)],
                  [0, 0, 1]])

    return np.dot(R, u)


# 縮小 -> 植えるときの幅、何条植えかなどの情報をもとに配列を縮小する処理
def paddy_shrink(u, xShrink, yShrink):
    R = np.array([[xShrink, 0, 0],
                  [0, yShrink, 0],
                  [0, 0, 1]])

    return np.dot(R, u)


# 多角形の外周について、縮小を行った、内周を算出。
# x, y軸において、各辺から1を引いた値が内周になると仮定できる。
# 内周の配列を作る必要があるのかもしれない。
def inside_paddy(u, x_shrink, y_shrink):
    R = np.array([[x_shrink, 0, 1],
                  [0, y_shrink, -1],
                  [0, 0, 1]])

    return np.dot(R, u)


# positionがpolygonのどの点と近いのかindexを返す
def most_close_index(position, polygon):
    distance_list = []
    for x, y in polygon:
        b = (x, y)
        distance_list.append(distance.euclidean(position, b))
    return distance_list.index(min(distance_list))


def position_to_position_distance(now_position, next_position, door_way_position):
    ptp_distance1 = distance.euclidean(now_position, door_way_position)
    ptp_distance2 = distance.euclidean(now_position, next_position)
    # 次のポジションと出入り口のpositionの距離を比較して、より近い方を返す
    if ptp_distance1 < ptp_distance2:
        return door_way_position
    else:
        return next_position


def position_in_line(position, polygon):
    for i in range(len(polygon)):
        a = polygon[i - 1]
        b = polygon[i]
        print((position[1] * (a[0] - b[0])) + (a[1] * (b[0] - position[0])) + (b[1] * (position[0] - a[0])))
        if (a[0] <= position[0] <= b[0]) or (b[0] <= position[0] <= a[0]):
            if (a[1] <= position[1] <= b[1]) or (b[1] <= position[1] <= a[1]):
                if (position[1] * (a[0] - b[0])) + (a[1] * (b[0] - position[0])) + (b[1] * (position[0] - a[0])) == 0:
                    # 点Pが線分AB上にある
                    return True, a, b

    # 点Pが線分AB上にない
    return False, 0, 0
