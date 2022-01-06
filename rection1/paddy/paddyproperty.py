import math
import numpy as np

from .routeProposal import RouteProposal as rp
from rection1.paddy.Model.paddyModel import Paddy, Position
from geopy.distance import geodesic
from ..paddy.Model.machineModel import Machine
from rection1.paddy.Parameters import paddyParameters as pp
from ..util import util


"""
memo
次回の作業:

"""


class PaddyProperty:
    # 外周の縦横の長さを格納
    outsideMaxRow: int
    outsideMaxColumn: int

    # 内周の縦横の長さを格納
    insideMaxRow: int
    insideMaxColumn: int

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

    # 外周の配列を格納
    insidePaddyArray: list[list[any]]

    # 内周の配列を格納
    outsidePaddyArray: list[any]

    # 田んぼのポジションからポジションからまでの距離を格納
    paddyDistance: list[list[float]]

    # 機械の情報を格納
    machineInfo: Machine

    # 点から点までの移動量を格納
    xMovement: list[int]
    yMovement: list[int]

    # 作成したTOPからつながるノードを格納
    topToEndNode: list[int]

    # 原点のポジションを格納する
    topLeft: tuple

    # 田んぼの[外周]のポジションが2次元配列のどこにあるのかを格納
    # 原点からそれぞれのポジションへの距離を格納
    # 実質各ポジションがlistのどこにあるのかを示すこととなる
    outsideCircumferenceRowList: list[int]
    outsideCircumferenceColumnList: list[int]

    # 田んぼの[内周]のポジションが2次元配列のどこにあるのかを格納
    # 実質各ポジションがlistのどこにあるのかを示すこととなる
    insideCircumferenceRowList: list[int]
    insideCircumferenceColumnList: list[int]

    # 出入口がどこにあるのかを格納
    doorwayColumnList: list[int]
    doorwayRowList: list[int]

    def __init__(self, paddyFields, startEndPosition, machineInfo):
        # 必要な情報の初期化
        # 引数にある情報を初期化
        self.paddyFields = paddyFields
        self.startEndPosition = startEndPosition
        self.machineInfo = machineInfo

        # 単独で呼び出し可能
        # 必要な値を生成
        self.generateRequiredParameters()
        # ポジションからポジションまでの長さを算出
        self.generatePtPDistance()

        # リストを生成
        self.createList()

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
        self.generateOutside()
        self.generateNewMovementAndCorrection()
        # 内周のポジションを確定させる
        self.generateInside()

    # 点と点の距離情報を算出
    def generatePtPDistance(self):

        #   距離情報を格納するリストを生成
        paddyDistance = [[0.0 for _ in range(len(self.paddyFields))] for _ in range(len(self.paddyFields))]

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
                yMovement.append(round(-1 * y))
                yPCount += 1
            else:
                yMovement.append(round(y))
                yMCount += 1

            #   横の計算現在のポジションのtempのポジションから次のポジションを引いて
            #   「正」なら今のポジションは次のポジションより右である
            if (tempPosition[1] - nextPosition[1]) < 0:
                xMovement.append(round(x))
                xPCount += 1
            else:
                xMovement.append(round(-1 * x))
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
            xMove = self.outsideCircumferenceColumnList[i] - xMove
            yMove = self.outsideCircumferenceRowList[i] - yMove
        self.xMovement = xMovement
        self.yMovement = yMovement

    # 各ノードがつながっているリストを作成
    def generateTopToEndNodeList(self):
        nodeList = []
        for i in range(0, len(self.xMovement)):
            index = self.topIndex + i
            if index >= len(self.xMovement):
                index -= len(self.xMovement)
            nodeList.append(index)
        self.topToEndNode = nodeList

    # ポリゴンのポジションを特定
    def generateOutside(self):
        columnArray = []
        rowArray = []
        doorwayColumnList = []
        doorwayRowList = []

        for i in self.paddyFields:
            edge = i.y, self.topLeft[1]
            position = i.y, i.x
            columnArray.append(round(math.ceil(geodesic(edge, position).m * 100)))

            edge = self.topLeft[0], i.x
            position = i.y, i.x
            rowArray.append(round(math.ceil(geodesic(edge, position).m * 100)))
        for i in self.startEndPosition:
            edge = i.y, self.topLeft[1]
            position = i.y, i.x
            doorwayColumnList.append(
                round(math.ceil(geodesic(edge, position).m * 100)))

            edge = self.topLeft[0], i.x
            position = i.y, i.x
            doorwayRowList.append(round(math.ceil(geodesic(edge, position).m * 100)))

        # ポジションの情報を格納
        self.outsideCircumferenceRowList = rowArray
        self.outsideCircumferenceColumnList = columnArray

        # ポジションの行の場所を格納
        self.doorwayColumnList = doorwayColumnList
        self.doorwayRowList = doorwayRowList

        # ポリゴンを回転させる
        self.changeAngle()

        # ポリゴンを縮小させる
        self.paddyShrink()

        # 一番右にあるポジションのindexを取得
        self.arrayRightIndex = columnArray.index(max(columnArray))
        # 一番左にあるポジションのindexを取得
        self.arrayLeftIndex = columnArray.index(min(columnArray))
        # 一番上にあるポジションのindexを取得
        self.arrayTopIndex = rowArray.index(min(rowArray))
        # 一番下にあるポジションのindexを取得
        self.arrayBottomIndex = rowArray.index(max(rowArray))

        # 一番左の値が負になる可能性があるためその調整を行う
        if self.outsideCircumferenceColumnList[self.arrayLeftIndex] < 0:
            move = self.outsideCircumferenceColumnList[self.arrayLeftIndex]
            for i in self.topToEndNode:
                after = self.outsideCircumferenceColumnList[i] - move
                self.outsideCircumferenceColumnList[i] = after

            for i in range(len(self.doorwayColumnList)):
                after = self.doorwayColumnList[i] - move
                self.doorwayColumnList[i] = after

        # 縦と横を算出
        self.outsideMaxRow = round(max(self.outsideCircumferenceRowList) + self.yCorrection)
        self.outsideMaxColumn = round(max(self.outsideCircumferenceColumnList) + self.xCorrection)

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
        if self.topIndex < topToLeft:
            turnClock = True

        topY = -1 * self.outsideCircumferenceRowList[self.topIndex]
        topX = self.outsideCircumferenceColumnList[self.topIndex]
        top = np.array([topX, topY])

        topToLeftY = -1 * self.outsideCircumferenceRowList[topToLeft]
        topToLeftX = self.outsideCircumferenceColumnList[topToLeft]
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

        for index in self.topToEndNode:
            y = -1 * self.outsideCircumferenceRowList[index]
            x = self.outsideCircumferenceColumnList[index]
            moveNode = np.array([x, y, 1])
            if turnClock:
                # 時計回りで回転させる
                rad = -1 * rad
            x, y, z = util.rotation_o(moveNode, rad, topX, topY)
            self.outsideCircumferenceRowList[index] = round(-1 * y)
            self.outsideCircumferenceColumnList[index] = round(x)

        # 配列の中のどこに出入り口があるのかを特定し回転させたあとの配列の位置
        for index in range(len(self.doorwayColumnList)):
            y = -1 * self.doorwayRowList[index]
            x = self.doorwayColumnList[index]
            moveNode = np.array([x, y, 1])
            if turnClock:
                # 時計回りで回転させる
                rad = -1 * rad
            x, y, z = util.rotation_o(moveNode, rad, topX, topY)
            self.doorwayRowList[index] = round(-1 * y)
            self.doorwayColumnList[index] = round(x)

    # 田んぼを縮小する
    def paddyShrink(self):
        for index in self.topToEndNode:
            y = -1 * self.outsideCircumferenceRowList[index]
            x = self.outsideCircumferenceColumnList[index]
            moveNode = np.array([x, y, 1])
            x, y, z = util.paddyShrink(
                moveNode,
                1 / self.machineInfo.BetweenTheLines,
                1 / self.machineInfo.BetweenStocks
            )
            self.outsideCircumferenceRowList[index] = round(-1 * y)
            self.outsideCircumferenceColumnList[index] = round(x)
        # 配列の中のどこに出入り口があるのかを特定し回転させたあとの配列の位置
        for index in range(len(self.doorwayColumnList)):
            y = -1 * self.doorwayRowList[index]
            x = self.doorwayColumnList[index]
            moveNode = np.array([x, y, 1])
            x, y, z = util.paddyShrink(
                moveNode,
                1 / self.machineInfo.BetweenTheLines,
                1 / self.machineInfo.BetweenStocks
            )
            self.doorwayRowList[index] = round(-1 * y)
            self.doorwayColumnList[index] = round(x)

    # 移動量を算出後に呼び出せる。
    def checkClockWise(self):
        # 正なら時計回り
        if self.xMovement[self.topIndex] > 0:
            self.clockWise = True

    # 内周のポジションを確定させる
    def generateInside(self):
        insideRowList = []
        insideColumnList = []
        rowList = self.outsideCircumferenceRowList
        columnList = self.outsideCircumferenceColumnList

        # 各外周のポジションの斜めに位置するところがポリゴンの内周にあるのかを判別する
        for i in self.topToEndNode:
            diagonal = [
                (-1, -1),
                (-1, 1),
                (1, -1),
                (1, 1)
            ]
            for j in diagonal:
                row = self.outsideCircumferenceRowList[i] + j[0]
                column = self.outsideCircumferenceColumnList[i] + j[1]
                if util.isPositionInsidePolygon(rowList, columnList, column, row):
                    insideRowList.append(row)
                    insideColumnList.append(column)
                    break
        self.insideCircumferenceRowList = insideRowList
        self.insideCircumferenceColumnList = insideColumnList

        self.insideMaxRow = max(self.insideCircumferenceRowList)
        self.insideMaxColumn = max(self.insideCircumferenceColumnList)

        # 配列を生成

    def createList(self):
        #   配列の生成   列、行で生成
        paddyArray = [
            [0] * (self.outsideMaxColumn + self.xCorrection)
            for _ in range(self.outsideMaxRow + self.yCorrection)
        ]
        outside = [[0] * self.outsideMaxColumn
                   for _ in range(3)]

        inside = [0 for _ in range(self.outsideMaxColumn - 2)]

        self.paddyArray = paddyArray
        # 回転後のポジション情報を配列に描画
        for index in self.topToEndNode:
            util.fillPaddy(
                self.paddyArray,
                self.outsideCircumferenceRowList[index],
                self.outsideCircumferenceColumnList[index],
                pp.OUTSIDE_POSITION)

        for index in range(len(self.doorwayColumnList)):
            if self.startEndPosition[index].position == "start":
                util.fillPaddy(
                    self.paddyArray,
                    self.doorwayRowList[index],
                    self.doorwayColumnList[index],
                    pp.START_POSITION
                )
            else:
                util.fillPaddy(
                    self.paddyArray,
                    self.doorwayRowList[index],
                    self.doorwayColumnList[index],
                    pp.END_POSITION
                )
        for inside in range(len(self.insideCircumferenceRowList)):
            util.fillPaddy(
                self.paddyArray,
                self.insideCircumferenceRowList[inside],
                self.insideCircumferenceColumnList[inside],
                pp.INSIDE_POSITION
            )
        util.exportToFile(paddyArray)

        rs = rp(
            paddyArray=self.paddyArray,
            doorwayRowList=self.doorwayRowList,
            doorwayColumnList=self.doorwayColumnList,
            insideRowList=self.insideCircumferenceRowList,
            insideColumnList=self.insideCircumferenceColumnList,
            outsideRowList=self.outsideCircumferenceRowList,
            outsideColumnList=self.outsideCircumferenceColumnList,
            outside=outside,
            inside=inside,
            machineInfo=self.machineInfo
        )
        rs.searchRoute()
