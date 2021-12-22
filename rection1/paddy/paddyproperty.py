import csv

from .parameter import Paddy, Position
import math
from geopy.distance import geodesic

JOUKAN: int = 30
KABUMA: int = 18
POSITION = 5
WALL = 4


class PaddyProperty:
    # 縦横の長さを格納
    vertical: int
    beside: int

    # 上下左右の値を格納
    rightIndex: int
    leftIndex: int
    topIndex: int
    bottomIndex: int

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
    paddyArray: list[list[int]]

    # 田んぼのポジションからポジションからまでの距離を格納
    paddyDistance: list[list[float]]

    # 田んぼのポジションが2次元配列のどこにあるのかを格納
    xPositionList: list[int]
    yPositionList: list[int]

    # 点から点までの移動量を格納
    xMovement: list[int]
    yMovement: list[int]

    # ノードからノードまでの順番を格納
    nodeList: list[list[bool]]

    # 作成したTOPからつながるノードを格納
    topToEndNode: list[int]

    def __init__(self, paddyFields, startEndPosition):
        self.paddyFields = paddyFields
        self.startEndPosition = startEndPosition
        self.generateRequiredParameters()
        self.generateMovementCorrection()
        self.generatePtPDistance()
        self.createNodelist()
        self.createList()

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

        # 高さと底辺を算出
        self.vertical = round((geodesic(self.topVal, self.bottomVal).m * 100) / KABUMA)
        self.beside = round((geodesic(self.leftVal, self.rightVal).m * 100) / JOUKAN)

    def createNodelist(self):
        nodeList = []
        # ポジションから
        for i in range(len(self.paddyDistance)):
            node = []
            for j in range(len(self.paddyDistance)):
                if self.paddyDistance[i][j] > 0:
                    node.append(True)
                elif self.paddyDistance[i][j] == 0:
                    node.append(False)
            nodeList.append(node)
        self.nodeList = nodeList

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

    def generateMovementCorrection(self):
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

        self.xMovement = xMovement
        self.yMovement = yMovement
        self.yCorrection = yCount
        self.xCorrection = xCount

    def createList(self):
        #   配列の生成   列、行で生成
        tempPaddyArray = [[0] * (self.beside + self.xCorrection) for _ in range(self.vertical + self.yCorrection)]

        topMovement = 0
        # 左と上のポジションの番号を比較
        # もっとも高いポジションを取得する
        # 最も高い点を取得して、原点から右に動かす
        print("xの移動量", self.xMovement)
        print("yの移動量", self.yMovement)
        # 時計回りなのか反時計回りなのかを算出
        # clockWiseがTrueなら時計回り、Falseなら反時計回り
        if self.xMovement[self.topIndex] > 0:
            self.clockWise = True

        # 時計回りなら、頂点がらみのxMovementは必ず正
        # 反時計回りなら、頂点がらみのxMovementは必ず負
        if self.clockWise:
            print("時計回り")
            if self.topIndex < self.leftIndex:
                print("頂点が左よりIndexが小さい")
                print("一番高い点:", self.topIndex)
                print("一番左の点:", self.leftIndex)
                for i in range(self.leftIndex, len(self.xMovement)):
                    topMovement += self.xMovement[i]
                    print("topMovement timeLapse", topMovement)
                print("原点から右に", topMovement, "だけ移動")
            else:
                print("頂点が左よりIndexが大きい")
                print("一番高い点:", self.topIndex)
                print("一番左の点:", self.leftIndex)
                for i in range(self.leftIndex, self.topIndex):
                    topMovement += self.xMovement[i]
                    print("topMovement timeLapse", topMovement)
                    print(topMovement, "だけ移動")
        else:
            # 反時計回り
            print("反時計回り")
            if self.topIndex < self.leftIndex:
                print("頂点が左よりIndexが小さい")
                print("一番高い点:", self.topIndex)
                print("一番左の点:", self.leftIndex)
                for i in range(self.leftIndex, len(self.xMovement)):
                    topMovement += self.xMovement[i]
                    print("topMovement timeLapse", topMovement)
                print("原点から右に", topMovement, "だけ移動")
            else:
                print("頂点が左よりIndexが大きい")
                print("一番高い点:", self.topIndex)
                print("一番左の点:", self.leftIndex)
                for i in range(self.leftIndex, self.topIndex):
                    topMovement += self.xMovement[i]
                    print("topMovement timeLapse", topMovement)
                    print(topMovement, "だけ移動")
        self.paddyArray = tempPaddyArray
        self.generateWallPositionList(topMovement)
        return self.paddyArray

    def generateWallPositionList(self, topMovement):
        yPosition = 0
        xPosition = topMovement

        nodeList = []
        yPositionList = []
        xPositionList = []

        for i in range(0, len(self.xMovement)):
            index = self.topIndex + i
            if index >= len(self.xMovement):
                index -= len(self.xMovement)
            xPosition += self.xMovement[index]
            yPosition += self.yMovement[index]
            if xPosition < 0:
                xPosition = 0
            if yPosition < 0:
                yPosition = 0
            xPositionList.append(xPosition)
            yPositionList.append(yPosition)
            nodeList.append(index)
        self.xPositionList = xPositionList
        self.yPositionList = yPositionList
        self.topToEndNode = nodeList
        print("xPositionList", xPositionList)
        print("yPositionList", yPositionList)
        print("nodeList", nodeList)

        self.generatePosition()

    def generatePosition(self):
        for i in range(len(self.xPositionList)):
            print(self.yPositionList[i-1], self.xPositionList[i-1], "ポジション")
            self.paddyArray[self.yPositionList[i]][self.xPositionList[i]] = POSITION
        if self.clockWise:
            print("時計回り")
            for i in self.topToEndNode:
                self.generateWall(
                    self.xMovement[self.topToEndNode[i]],
                    self.yMovement[self.topToEndNode[i]],
                    self.xPositionList[i - 1],
                    self.yPositionList[i - 1],
                    i
                )
        else:
            print("反時計回り")
            for i in range(len(self.topToEndNode)):
                self.generateWall(
                    self.xMovement[self.topToEndNode[i]],
                    self.yMovement[self.topToEndNode[i]],
                    self.xPositionList[i - 1],
                    self.yPositionList[i - 1],
                    self.topToEndNode[i]
                )
        print(*self.paddyArray, sep="\n")
        # 外周の情報をpaddyArray.csvに保存
        # with open('C:/Users/196009/Desktop/paddyArray.csv', 'w', encoding='UTF-8') as f:
        #     writer = csv.writer(f, lineterminator='\n')
        #     writer.writerows(self.paddyArray)

    def generateWall(self, xMovement, yMovement, xPosition, yPosition, node):
        # 傾き
        a = yMovement / xMovement
        xMovementTo = xPosition + xMovement
        yMovementTo = yPosition + yMovement
        print("縦", self.vertical)
        print("横", self.beside)
        print(node)
        if xMovement > 0:
            # 現在のポジションを原点として、右に進む
            print("xMovementは正")
            print("傾き", a)
            print("yPosition", yPosition)
            print("xPosition", xPosition)
            print("y軸の移動量", yMovement)
            print("x軸の移動量", xMovement)
            print("x軸移動後のポジション", xMovementTo)
            print("y軸移動後のポジション", yMovementTo)
            print(range(0, xMovement, 1))
            for x in range(0, xMovement, 1):
                self.drawWall(a, x, xPosition, yPosition, yMovement > 0)
        else:
            # 現在のポジションを原点として、左に進む
            print("xMovementは負")
            print("傾き", a)
            print("yPosition", yPosition)
            print("xPosition", xPosition)
            print("y軸の移動量", yMovement)
            print("x軸の移動量", xMovement)
            print("x軸移動後のポジション", xMovementTo)
            print("y軸移動後のポジション", yMovementTo)
            print(range(0, xMovement, -1))
            for x in range(0, xMovement, -1):
                self.drawWall(a, x, xPosition, yPosition, yMovement > 0)

    def drawWall(self, a, x, xPosition, yPosition, flag):
        y = a * x
        yTo = yPosition + math.floor(y)
        xTo = xPosition + x
        # if flag:

        print("paddy[", yTo, "][", xTo, "]")
        if self.paddyArray[yTo][xTo] == 0:
            self.paddyArray[yTo][xTo] = WALL

        #     for x in range(xPositionList[node[0]] + 1, xPositionList[node[1]] + 1, 1):
        #         y = a * (xPositionList[node[0]] - x)
        #         print("yの値", y)
        #         print("xの値", x)
        #         y = yPositionList[node[0]] + math.floor(y)
        #         print("yの値加工後", y)
        #         print("paddyArray[", y, "][", x, "]を壁とする")
        #         if self.paddyArray[y][x] == 0:
        #             self.paddyArray[y][x] = WALL
        # else:
        #     for x in range(xPositionList[node[0]] - 1, xPositionList[node[1]], -1):
        #         y = a * (xPositionList[node[0]] - x)
        #         print("yの値", y)
        #         print("xの値", xPositionList[node[0]] - x)
        #         y = yPositionList[node[0]] + math.floor(y)
        #         print("yの値加工後", y)
        #         print("paddyArray[", y, "][", x, "]を壁とする")
        #         if self.paddyArray[y][x] == 0:
        #             self.paddyArray[y][x] = WALL
        # return self.paddyArray
