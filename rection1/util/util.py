import hashlib
import csv
import math
import numpy as np

from ..models import User
from sympy.geometry import Point, Polygon
from ..exception import Exception
from ..paddy.Parameters import paddyParameters as pp


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


def isPositionInsidePolygon(rowList, columnList, x, y) -> bool:
    points = []

    # ポリゴンのポジション情報を取得
    for i in range(len(rowList)):
        p = Point(columnList[i], rowList[i])
        points.append(p)
    poly = Polygon(*points)

    point = Point(x, y)

    return poly.encloses_point(point)


def fillPaddy(paddyArray, row, column, string):
    row = math.floor(row)
    column = math.floor(column)
    if string == pp.OUTSIDE_POSITION:
        print("paddy[", row, "][", column, "]が外周")
    elif string == pp.INSIDE_POSITION:
        print("paddy[", row, "][", column, "]が内周")
    elif string == pp.START_POSITION:
        print("paddy[", row, "][", column, "]が入口")
    elif string == pp.END_POSITION:
        print("paddy[", row, "][", column, "]が出口")

    if paddyArray[row][column] == 0:
        paddyArray[row][column] = string
    else:
        print("paddyArray[", row, "][", column, "]is not void")


def exportToFile(paddyArray, fileName='paddyArray'):
    filePath = 'C:/Users/196009/Desktop/' + fileName + '.csv'
    print(filePath, "に書き込み中")
    with open(filePath, 'w', encoding='UTF-8') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(paddyArray)
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


def paddyShrink(u, xShrink, yShrink):
    R = np.array([[xShrink, 0, 0],
                  [0, yShrink, 0],
                  [0, 0, 1]])

    return np.dot(R, u)

