import csv

from .paddyParameter import Paddy, Position
import math
from geopy.distance import geodesic
from sympy.geometry import Point, Polygon
from ..exception import Exception
import numpy as np

JOUKAN: int = 30
KABUMA: int = 18
START_POSITION = "S"
END_POSITION = "E"
POSITION = "P"
WALL = "W"
INSIDE = "I"

"""
memo
次回の作業:

xMovementとyMovementもこの仕様変更を受けて、処理を変更する必要があるため、それを行う。
"""


class PaddyProperty:
    # 縦横の長さを格納
    maxRow: int
    maxColumn: int

    # 上下左右の値を格納
    rightIndex: int
    leftIndex: int
    topIndex: int
    bottomIndex: int

    # 回転後の上下左右の値を格納
    arrayRightIndex: int
    arrayLeftIndex: int
    arrayTopIndex: int
    arrayBottomIndex: int

    # 上下の座標を格納
    topVal: tuple
    bottomVal: tuple

    # 横の座標を格納
    leftVal: tuple
    rightVal: tuple

    # 縦横の補正数を格納
    yCorrection: int
    xCorrection: int

    # 時計回り
    clockWise: bool = False

    # 始点終点の情報
    startEndPosition: list[Position]

    # 田んぼの座標情報
    paddyFields: list[Paddy]

    # 田んぼの配列を格納
    paddyArray: list[list[any]]

    # 田んぼのポジションからポジションからまでの距離を格納
    paddyDistance: list[list[float]]

    # 田んぼのポジションが2次元配列のどこにあるのかを格納
    rowList: list[int]
    columnList: list[int]

    # 点から点までの移動量を格納
    xMovement: list[int]
    yMovement: list[int]

    # 作成したTOPからつながるノードを格納
    topToEndNode: list[int]

    # 原点のポジションを格納する
    topLeft: tuple

    # 原点からそれぞれのポジションへの距離を格納
    # 実質各ポジションがlistのどこにあるのかを示すこととなる
    rowList: list[int]
    columnList: list[int]

    def __init__(self, paddyFields, startEndPosition):
        self.paddyFields = paddyFields
        self.startEndPosition = startEndPosition

        # 単独で呼び出し可能
        self.generateRequiredParameters()
        self.generatePtPDistance()

        self.createList()

        self.fillWall()
        # 最後に呼び出す
        # self.generatePerimeter()

    # 必要なパラメータを算出
    def generateRequiredParameters(self):
        xList = []
        yList = []

        for i in self.paddyFields:
            xList.append(i.x)
            yList.append(i.y)

        # 一番右にあるポジションのindexを取得
        self.rightIndex = xList.index(max(xList))
        # 一番左にあるポジションのindexを取得
        self.leftIndex = xList.index(min(xList))
        # 一番上にあるポジションのindexを取得
        self.topIndex = yList.index(max(yList))
        # 一番下にあるポジションのindexを取得
        self.bottomIndex = yList.index(min(yList))

        # 高さを算出するために必要な処理
        self.topVal = yList[self.topIndex], xList[self.topIndex]
        self.bottomVal = yList[self.bottomIndex], xList[self.topIndex]

        # 底辺を算出するために必要な処理
        self.leftVal = yList[self.rightIndex], xList[self.rightIndex]
        self.rightVal = yList[self.rightIndex], xList[self.leftIndex]

        # 左上の座標を格納
        self.topLeft = yList[self.topIndex], xList[self.leftIndex]

        self.generateMovementAndCorrection()
        self.generateWallPositionList()
        self.generateNewMovementAndCorrection()

    # 点と点の距離情報を算出
    def generatePtPDistance(self):

        #   距離情報を格納するリストを生成
        paddyDistance = [[0.0 for i in range(len(self.paddyFields))] for j in range(len(self.paddyFields))]

        start_point = (self.paddyFields[0].y, self.paddyFields[0].x)
        end_point = (self.paddyFields[len(self.paddyFields) - 1].y, self.paddyFields[len(self.paddyFields) - 1].x)

        paddyDistance[0][len(self.paddyFields) - 1] = math.ceil(geodesic(start_point, end_point).m * 100)
        paddyDistance[len(self.paddyFields) - 1][0] = math.ceil(geodesic(end_point, start_point).m * 100)

        for i in range(1, len(self.paddyFields)):
            nowPosition = (self.paddyFields[i - 1].y, self.paddyFields[i - 1].x)
            nextPosition = (self.paddyFields[i].y, self.paddyFields[i].x)
            paddyDistance[i - 1][i] = math.ceil(geodesic(nowPosition, nextPosition).m * 100)
            paddyDistance[i][i - 1] = math.ceil(geodesic(nextPosition, nowPosition).m * 100)

        self.paddyDistance = paddyDistance

    # 行、列軸の移動量を算出
    def generateMovementAndCorrection(self):
        xMovement = []
        yMovement = []
        yPCount = 0
        yMCount = 0
        xPCount = 0
        xMCount = 0
        yCount = 0
        xCount = 0

        for i in range(len(self.paddyFields)):
            if i < (len(self.paddyFields) - 1):
                startPosition = self.paddyFields[i].y, self.paddyFields[i].x
                nextPosition = self.paddyFields[i + 1].y, self.paddyFields[i + 1].x
                tempPosition = self.paddyFields[i + 1].y, self.paddyFields[i].x
            else:
                startPosition = self.paddyFields[i].y, self.paddyFields[i].x
                nextPosition = self.paddyFields[0].y, self.paddyFields[0].x
                tempPosition = self.paddyFields[0].y, self.paddyFields[i].x

            #   startからnextまでの縦と横の距離をcmで取得
            x = geodesic(tempPosition, nextPosition).m * 100
            y = geodesic(startPosition, tempPosition).m * 100

            #   配列の必要数を算出
            #   配列のベクトルを決定する
            #   縦の計算, 現在のポジションから次のポジションのtempのポジションを引いて
            #   「正」なら今のポジションは次のポジションより下である
            if (startPosition[0] - tempPosition[0]) < 0:
                yMovement.append(round(-1 * (y / KABUMA)))
                yPCount += 1
            else:
                yMovement.append(round((y / KABUMA)))
                yMCount += 1

            #   横の計算現在のポジションのtempのポジションから次のポジションを引いて
            #   「正」なら今のポジションは次のポジションより右である
            if (tempPosition[1] - nextPosition[1]) < 0:
                xMovement.append(round(x / JOUKAN))
                xPCount += 1
            else:
                xMovement.append(round(-1 * (x / JOUKAN)))
                xMCount += 1

            if yPCount < yMCount:
                yCount = yMCount
            else:
                yCount = yPCount

            if xPCount < xMCount:
                xCount = xMCount
            else:
                xCount = xPCount

        # 縦横の移動量
        self.xMovement = xMovement
        self.yMovement = yMovement
        # 補正値
        self.yCorrection = yCount
        self.xCorrection = xCount
        # 最も高いノードから順番を算出
        self.generateTopToEndNodeList()
        self.checkClockWise()

    # 配列が変更されたことによって移動量に変更が起こる
    def generateNewMovementAndCorrection(self):
        xMovement = []
        yMovement = []
        xMove = 0
        yMove = 0
        for i in self.topToEndNode:
            xMove = self.columnList[i] - xMove
            yMove = self.rowList[i] - yMove

            xMovement.append(xMove)
            yMovement.append(yMove)
        self.xMovement = xMovement
        self.yMovement = yMovement
        print()
        print("列のリスト", self.columnList)
        print("行のリスト", self.rowList)
        print("列移動量", xMovement)
        print("行移動量", yMovement)

    # 配列を生成

    def createList(self):
        #   配列の生成   列、行で生成
        self.paddyArray = [[0] * (self.maxColumn + self.xCorrection) for _ in range(self.maxRow + self.yCorrection)]

    # 各ノードがつながっているリストを作成
    def generateTopToEndNodeList(self):
        nodeList = []
        for i in range(0, len(self.xMovement)):
            index = self.topIndex + i
            if index >= len(self.xMovement):
                index -= len(self.xMovement)
            nodeList.append(index)
        self.topToEndNode = nodeList

    # 壁を描画する最初のメソッド
    def generatePerimeter(self):
        for i in range(len(self.rowList)):
            self.paddyArray[self.rowList[i]][self.columnList[i]] = POSITION

        print("行の移動量", self.yMovement)
        print("列の移動量", self.xMovement)
        if self.clockWise:
            # print("時計回り")
            for i in self.topToEndNode:
                self.generateWall(
                    self.yMovement[self.topToEndNode[i]],
                    self.xMovement[self.topToEndNode[i]],
                    self.rowList[i],
                    self.columnList[i],
                    i
                )
        else:
            # print("反時計回り")
            for i in range(len(self.topToEndNode)):
                self.generateWall(
                    self.yMovement[self.topToEndNode[i]],
                    self.xMovement[self.topToEndNode[i]],
                    self.rowList[i],
                    self.columnList[i],
                    self.topToEndNode[i]
                )
        # print(*self.paddyArray, sep="\n")
        # 外周の情報をpaddyArray.csvに保存
        with open('C:/Users/196009/Desktop/paddyArray.csv', 'w', encoding='UTF-8') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(self.paddyArray)

    # 壁を描画
    def generateWall(self, column, row, yPosition, xPosition, node):
        # 傾き
        a = column / row
        xMovementTo = yPosition + row
        yMovementTo = xPosition + column
        yTo = yPosition
        print("列", column)
        print("行", row)
        # print(node)
        #
        # print("傾き", a)
        # print("yPosition", yPosition)
        # print("xPosition", xPosition)
        # print("y軸の移動量", yMovement)
        # print("x軸の移動量", xMovement)
        # print("x軸移動後のポジション", xMovementTo)
        # print("y軸移動後のポジション", yMovementTo)
        if column > 0:
            # 現在のポジションを原点として、右に進む
            # print("xMovementは正")
            # print(range(0, xMovement, 1))
            for x in range(0, column + 1, 1):
                yTo = self.drawWall(a, x, yPosition, xPosition, yTo)
                print(*self.paddyArray, sep="\n")
        else:
            # 現在のポジションを原点として、左に進む
            # print("xMovementは負")
            # print(range(0, xMovement, -1))
            for x in range(0, column - 1, -1):
                yTo = self.drawWall(a, x, yPosition, xPosition, yTo)
                print(*self.paddyArray, sep="\n")

    # 壁を描画
    def drawWall(self, a, x, yPosition, xPosition, yNow):
        y = a * x
        yTo = yPosition + math.floor(y)
        xTo = xPosition + x
        print("x軸", x)
        print("x移動", xTo)
        print("y軸", y)
        print("y移動", yTo)
        print("傾き", a)
        print("yの今の値", yNow)

        print("行", self.rowList)
        print("列", self.columnList)
        print()

        # if a == 0 だったときの処理を書く
        if a > 0:
            # 傾きが正(y > 0)なら右斜め下、左斜め上
            if yNow < yTo:
                # 右斜め下なら現在の値から向かう先の値を比較したとき
                # yNowはyToより小さくなる(yNow < yTo)
                # yは下に行くにつれて値は大きくなる。
                # yNowからyToに向かって行くため➘

                if 1 > a > -1:
                    for i in range(yNow, yTo):
                        print("傾きは小数点、paddy[", yNow + 1, "][", xTo - 1, "]")
                        if self.paddyArray[i + 1][xTo - 1] == 0:
                            self.paddyArray[i + 1][xTo - 1] = WALL
                    else:
                        print("for の中身を終了, 右斜め下")
                else:
                    print(range(yNow, yTo))
                    for i in range(yNow, yTo):
                        print("paddy[", i, "][", xTo - 1, "]")
                        if self.paddyArray[i][xTo - 1] == 0:
                            self.paddyArray[i][xTo - 1] = WALL
                    else:
                        print("for の中身を終了, 右斜め下")
            else:
                # 右斜め上なら現在の値から向かう先の値を比較したとき
                # yNowはyToより大きくなる(yNow > yTo)
                # yは上に行くにつれて値は小さくなる。
                # yNowからyToに向かって行くため↖
                if yTo < 0:
                    yTo = 0

                if 1 > a > -1:
                    for i in range(yNow, yTo, -1):
                        print("傾きは小数点、paddy[", i, "][", xTo + 1, "]")
                        if self.paddyArray[i][xTo + 1] == 0:
                            self.paddyArray[i][xTo + 1] = WALL
                    else:
                        print("for の中身を終了, 左斜め上")
                else:
                    print(range(yNow, yTo, -1))
                    for i in range(yNow, yTo, -1):
                        print("paddy[", i, "][", xTo + 1, "]")
                        if self.paddyArray[i][xTo + 1] == 0:
                            self.paddyArray[i][xTo + 1] = WALL
                    else:
                        print("for の中身を終了, 左斜め上")
        else:
            # 傾きが負(y < 0)なら右斜め上、左斜め下
            if yNow < yTo:
                # 右斜め下なら現在の値から向かう先の値を比較したとき
                # yNowはyToより小さくなる(yNow < yTo)
                # yは下に行くにつれて値は大きくなる。
                # yNowからyToに向かって行くため↘

                if 1 > a > -1:
                    for i in range(yNow, yTo):
                        print("傾きは小数点、paddy[", i + 1, "][", xTo, "]")
                        if self.paddyArray[i + 1][xTo] == 0:
                            self.paddyArray[i + 1][xTo] = WALL
                    else:
                        print("for の中身を終了, 左斜め下")
                else:
                    print(range(yNow, yTo))
                    for i in range(yNow, yTo):
                        print("paddy[", i + 1, "][", xTo, "]")
                        if self.paddyArray[i + 1][xTo] == 0:
                            self.paddyArray[i + 1][xTo] = WALL
                    else:
                        print("for の中身を終了, 左斜め下")
            else:
                # 右斜め上なら現在の値から向かう先の値を比較したとき
                # yNowはyToより大きくなる(yNow > yTo)
                # yは上に行くにつれて値は小さくなる。
                # yNowからyToに向かって行くため↗

                if yTo < 0:
                    yTo = 0

                if 1 > a > -1:
                    for i in range(yNow, yTo, -1):
                        print("傾きは小数点、paddy[", i + 1, "][", xTo, "]")
                        if self.paddyArray[i + 1][xTo] == 0:
                            self.paddyArray[i + 1][xTo] = WALL
                    else:
                        print("for の中身を終了, 右斜め上")
                else:
                    print(range(yNow, yTo, -1))
                    for i in range(yNow, yTo, -1):
                        print("paddy[", i, "][", xTo, "]")
                        if self.paddyArray[i][xTo] == 0:
                            self.paddyArray[i][xTo] = WALL
                    else:
                        print("for の中身を終了, 右斜め上")
        return yTo

    # ポリゴンのポジションを特定
    def generateWallPositionList(self):
        rowArray = []
        columnArray = []
        for i in self.paddyFields:
            edge = i.y, self.topLeft[1]
            position = i.y, i.x
            columnArray.append(round(math.ceil(geodesic(edge, position).m * 100) / KABUMA))

            edge = self.topLeft[0], i.x
            position = i.y, i.x
            rowArray.append(round(math.ceil(geodesic(edge, position).m * 100) / JOUKAN))
        # ポジションの行の場所を格納
        self.rowList = rowArray

        # ポジションの列の場所を格納
        self.columnList = columnArray

        self.rowList.index(max(self.rowList))

        self.changeAngle()
        # 一番右にあるポジションのindexを取得
        self.arrayRightIndex = columnArray.index(max(columnArray))
        # 一番左にあるポジションのindexを取得
        self.arrayLeftIndex = columnArray.index(min(columnArray))
        # 一番上にあるポジションのindexを取得
        self.arrayTopIndex = rowArray.index(min(rowArray))
        # 一番下にあるポジションのindexを取得
        self.arrayBottomIndex = rowArray.index(max(rowArray))

    # 行と列のポジションを格納しているリストの最適化
    """
    回転行列を用いて最も高い点(以後topと呼ぶ)を中心としてtopから一つ右の点(以後topLeftとする)をtopと同じ高さにするように変換を行う。
    アフィン変換を用いてこれを実現topを一度原点に移動させ、そこからtopからtopLeftへの角度(以後radとする)を算出、
    radをもとにそれぞれのポジションを同じradで反時計回りに回転させる。
    次回からはxMovementとyMovementもこの仕様変更を受けて、処理を変更する必要があるため、それを行う。
    """

    # 時計回りか反時計回りかを判定後呼び出し可能
    # ポリゴンを回転させる。
    def changeAngle(self):
        # 時計回りと反時計回りで処理を変えなければならない。
        # 時計回り
        # Yは行、Xは列
        turnClock = False

        if self.clockWise:
            topToLeft = self.topIndex + 1
        else:
            topToLeft = self.topIndex - 1
        if self.rowList[self.topIndex] < self.rowList[topToLeft]:
            turnClock = True

        topY = -1 * self.rowList[self.topIndex]
        topX = self.columnList[self.topIndex]
        top = np.array([topX, topY])

        topToLeftY = -1 * self.rowList[topToLeft]
        topToLeftX = self.columnList[topToLeft]
        topToLeft = np.array([topToLeftX, topToLeftY])

        topLeftTempY = topY
        topLeftTempX = topToLeftX
        topLeftTemp = np.array([topLeftTempX, topLeftTempY])

        # べクトルを定義
        vec_topLeftTemp = topLeftTemp - top
        vec_topToLeft = topToLeft - top

        # コサインの計算
        length_vec_topLeftTemp = np.linalg.norm(vec_topLeftTemp)
        length_vec_topToLeft = np.linalg.norm(vec_topToLeft)
        inner_product = np.inner(vec_topLeftTemp, vec_topToLeft)
        cos = inner_product / (length_vec_topLeftTemp * length_vec_topToLeft)

        # 角度（ラジアン）の計算 rad = Θ
        rad = np.arccos(cos)
        # print("行のリスト", self.rowList)
        # print("列のリスト", self.columnList)
        for index in self.topToEndNode:
            y = -1 * self.rowList[index]
            x = self.columnList[index]
            moveNode = np.array([x, y, 1])
            if turnClock:
                # 時計回りで回転させる
                rad = -1 * rad
            x, y, z = self.rotation_o(moveNode, rad, topX, topY)
            # print("(", round(x), round(-1 * y), ")")
            self.rowList[index] = round(-1 * y)
            self.columnList[index] = round(x)
        # print("移動後の行", self.rowList)
        # print("移動後の列", self.columnList)

        # 縦と横を算出
        self.maxRow = round(max(self.rowList) + self.yCorrection)
        self.maxColumn = round(max(self.columnList) + self.xCorrection)

    # 原点とする座標をx, yで渡す
    # 動かしたい座標をuで渡す
    # 最も高い点を中心に回転した後のx軸, y軸, z軸を返す
    @staticmethod
    def rotation_o(u, t, x, y, deg=False):

        # 度数単位の角度をラジアンに変換
        if deg:
            t = np.deg2rad(t)

        # 回転行列
        R = np.array([[np.cos(t), -np.sin(t), x - x * np.cos(t) + y * np.sin(t)],
                      [np.sin(t), np.cos(t), y - x * np.sin(t) - y * np.cos(t)],
                      [0, 0, 1]])
        return np.dot(R, u)

    # 移動量を算出後に呼び出せる。
    def checkClockWise(self):
        # 正なら時計回り
        if self.xMovement[self.topIndex] > 0:
            print(self.xMovement[self.topIndex])
            self.clockWise = True

    def fillWall(self):
        count = 0
        for y in range(self.rowList[self.arrayTopIndex], self.rowList[self.arrayBottomIndex]):
            for x in range(self.columnList[self.arrayLeftIndex], self.columnList[self.arrayRightIndex]):
                print(y, x, "を検査中")
                count += 1
                if self.isPositionInsidePolygon(self.rowList, self.columnList, x, y):
                    print(y, x, "はポリゴンの中にある")
                    self.fillPaddy(y, x, INSIDE)
                else:
                    pass
                    print(y, x, "はポリゴンの中にない")
        print(count, "回の捜索が行われた")
        self.exportToFile()

    # ポリゴンの中に存在するのかを調べる
    def isPointInPolygon(self):
        points = []

        # polygonの情報を取得
        for i in self.paddyFields:
            p = Point(i.x, i.y)
            points.append(p)
        poly = Polygon(*points)

        # 始点終点のポイントの情報を取得
        for i in self.startEndPosition:
            point = Point(i.x, i.y)
            if poly.encloses_point(point):
                pass
            else:
                raise Exception.PointException

    def isPositionInsidePolygon(self, rowList, columnList, x, y):
        points = []

        # ポリゴンのポジション情報を取得
        for i in self.topToEndNode:
            p = Point(columnList[i], rowList[i])
            points.append(p)
        poly = Polygon(*points)

        point = Point(x, y)

        return poly.encloses_point(point)

    def fillPaddy(self, row, column, string):
        if self.paddyArray[row][column] == 0:
            self.paddyArray[row][column] = string
        else:
            print("paddyArray[", row, "][", column, "]is not void")

    def exportToFile(self):
        print("ファイルpaddyArray.csvに書き込み中")
        with open('C:/Users/196009/Desktop/paddyArray.csv', 'w', encoding='UTF-8') as f:
            writer = csv.writer(f, lineterminator='\n')
            writer.writerows(self.paddyArray)
        print("ファイルpaddyArray.csvに書き込み完了")
