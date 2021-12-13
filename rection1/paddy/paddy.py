from geopy.distance import geodesic
from ..paddy.parameter import PaddyParameter
from ..paddy.paddyproperty import PaddyProperty
import math

JOUKAN: int = 1
KABUMA: int = 1
POSITION = "P"
WALL = "W"


#   位置情報を生成
def getPaddyFieldsPTPDistance(pram: PaddyParameter):
    paddyFields = pram.paddyFields
    pp = PaddyProperty(paddyFields)
    beside = pp.getBeside()
    print(beside)

#     xList = []
#     yList = []
#     nodeList = []
#
#     #   距離情報を格納するリストを生成
#     paddyArray = [[0.0 for i in range(len(paddyFields))] for j in range(len(paddyFields))]
#
#     paddyFields = pram.paddy
#     Fields
#     for i in paddyFields:
#         xList.append(i.x)
#         yList.append(i.y)
#
#     # 一番右にあるポジションのindexを取得
#     xMaxIndex = xList.index(max(xList))
#     # 一番左にあるポジションのindexを取得
#     xMinIndex = xList.index(min(xList))
#     # 一番上にあるポジションのindexを取得
#     yMaxIndex = yList.index(max(yList))
#     # 一番下にあるポジションのindexを取得
#     yMinIndex = yList.index(min(yList))
#
#     # 高さを算出するために必要な処理
#     topVal = yList[yMaxIndex], xList[yMaxIndex]
#     bottomVal = yList[yMinIndex], xList[yMaxIndex]
#
#     # 底辺を算出するために必要な処理
#     leftVal = yList[xMaxIndex], xList[xMaxIndex]
#     rightVal = yList[xMaxIndex], xList[xMinIndex]
#
#     # 高さと底辺を算出
#     vertical = round((geodesic(topVal, bottomVal).m * 100) / KABUMA)
#     beside = round((geodesic(leftVal, rightVal).m * 100) / JOUKAN)
#
#     # より大きい方を配列の数とする
#     if vertical > beside:
#         paddyList = [[0 for i in range(vertical)] for j in range(vertical)]
#     else:
#         paddyList = [[0 for i in range(beside)] for j in range(beside)]
#
#     # ポジションから
#     for i in range(len(paddyFields)):
#         if i + 1 == len(paddyFields):
#             tempNode = i, 0
#         else:
#             tempNode = i, i + 1
#         nodeList.append(tempNode)
#
#     start_point = (paddyFields[0].y, paddyFields[0].x)
#     end_point = (paddyFields[len(paddyArray) - 1].y, paddyFields[len(paddyArray) - 1].x)
#
#     paddyArray[0][len(paddyArray) - 1] = math.ceil(geodesic(start_point, end_point).m * 100)
#     paddyArray[len(paddyArray) - 1][0] = math.ceil(geodesic(end_point, start_point).m * 100)
#
#     for i in range(1, len(paddyArray)):
#         nowPosition = (paddyFields[i - 1].y, paddyFields[i - 1].x)
#         nextPosition = (paddyFields[i].y, paddyFields[i].x)
#
#         paddyArray[i - 1][i] = math.ceil(geodesic(nowPosition, nextPosition).m * 100)
#         paddyArray[i][i - 1] = math.ceil(geodesic(nextPosition, nowPosition).m * 100)
#
#     return paddyArray
#

#   点から点までのベクトル
def getPaddyFieldsPositionList(pram: PaddyParameter, paddyDistance):
    xMovement = []
    yMovement = []
    yPCount = 0
    yMCount = 0
    xPCount = 0
    xMCount = 0
    yCount = 0
    xCount = 0

    paddyFields = pram.paddyFields
    for i in range(len(paddyFields)):
        if i < (len(paddyFields) - 1):
            startPosition = paddyFields[i].y, paddyFields[i].x
            nextPosition = paddyFields[i + 1].y, paddyFields[i + 1].x
            tempPosition = paddyFields[i + 1].y, paddyFields[i].x
        else:
            startPosition = paddyFields[i].y, paddyFields[i].x
            nextPosition = paddyFields[0].y, paddyFields[0].x
            tempPosition = paddyFields[0].y, paddyFields[i].x

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

    vertical, beside, yMaxIndex, xMinIndex = searchMaxMin(pram, xCount, yCount)

    # paddyArray = createList(vertical, beside, yMaxIndex, xMinIndex, xMovement, yMovement)
    # print(*paddyArray, sep="\n")


#   配列を作成するための縦と横の値を算出
def searchMaxMin(pram: PaddyParameter, xCorrection, yCorrection):
    xList = []
    yList = []
    paddyFields = pram.paddyFields
    for i in paddyFields:
        xList.append(i.x)
        yList.append(i.y)

    xMaxIndex = xList.index(max(xList))
    xMinIndex = xList.index(min(xList))
    yMaxIndex = yList.index(max(yList))
    yMinIndex = yList.index(min(yList))

    topVal = yList[yMaxIndex], xList[yMaxIndex]
    bottomVal = yList[yMinIndex], xList[yMaxIndex]

    leftVal = yList[xMaxIndex], xList[xMaxIndex]
    rightVal = yList[xMaxIndex], xList[xMinIndex]

    vertical = round((geodesic(topVal, bottomVal).m * 100) / KABUMA) + yCorrection
    beside = round((geodesic(leftVal, rightVal).m * 100) / JOUKAN) + xCorrection
    return vertical, beside, yMaxIndex, xMinIndex


def createList(vertical, beside, yMaxIndex, xMinIndex, xMovement, yMovement):
    top = 0
    #   配列の生成
    paddyArray = [[0 for i in range(beside)] for j in range(vertical)]

    # 左と上のポジションの番号を比較
    # もっとも高いポジションを取得する
    if xMinIndex < yMaxIndex:
        print(xMinIndex, "から", yMaxIndex, "まで1ずつ")
        for i in range(xMinIndex, yMaxIndex):
            print(i, "番目")
            top += xMovement[i]
            print(top, "だけ移動")
    elif xMinIndex < yMaxIndex:
        pass
    else:
        print(xMinIndex - 1, "から", yMaxIndex - 1, "まで-1ずつ")
        for i in range(xMinIndex - 1, yMaxIndex - 1, -1):
            top += xMovement[i]
            print(top, "だけ移動")
        top = -1 * top
    paddyArray[0][top] = POSITION
    print("最も高いポジションである", yMaxIndex, "でリストの[0]", "[", top - 1, "]である")

    tate = 0
    yoko = top
    xPositionList = []
    yPositionList = []
    nodeList = []
    # print(*paddyArray, sep="\n")

    if yMaxIndex == 0:
        for i in range(1, len(xMovement)):
            tate += yMovement[i]
            yoko += xMovement[i]
            print("リストの縦", vertical)
            print("リストの横", beside)
            print("xリストの移動量", xMovement)
            print("yリストの移動量", yMovement)
            print("ポジション", i)
            print("縦の移動", tate)
            print("横の移動", yoko)
            print("paddyArray[", tate, "][", yoko, "]を壁とする")
            paddyArray[tate][yoko] = POSITION
            xPositionList.append(yoko)
            yPositionList.append(tate)
            if i + 1 == len(xMovement):
                tempNode = i, 0
            else:
                tempNode = i, i + 1
            nodeList.append(tempNode)
            print(*paddyArray, sep="\n")
    else:
        for i in range(0, len(xMovement)):
            temp = yMaxIndex
            tempI = -1 * len(xMovement) + temp + i
            yoko += xMovement[tempI]
            tate += yMovement[tempI]
            print("リストの縦", vertical)
            print("リストの横", beside)
            print("xリストの移動量", xMovement)
            print("yリストの移動量", yMovement)
            print("縦の移動量", xMovement[tempI])
            print("横の移動量", yMovement[tempI])
            print("ポジション", tempI)
            print("縦のリスト", tate)
            print("横のリスト", yoko)
            print("paddyArray[", tate, "][", yoko, "]を壁とする")
            paddyArray[tate][yoko] = POSITION
            xPositionList.append(yoko)
            yPositionList.append(tate)
            if tempI + 1 == len(xMovement):
                tempNode = tempI, 0
            else:
                tempNode = tempI, tempI + 1
            nodeList.append(tempNode)
            print(*paddyArray, sep="\n")

    # print(nodeList)

    #   ポジションを先頭に移動させる。
    firstXPosition = xPositionList[len(xPositionList) - 1]
    firstYPosition = yPositionList[len(yPositionList) - 1]
    xPositionList.remove(firstXPosition)
    xPositionList.insert(0, firstXPosition)
    yPositionList.remove(firstYPosition)
    yPositionList.insert(0, firstYPosition)

    #   それぞれのポジションを原点としたときのx, y軸の移動量を算出
    print(nodeList)
    for i in range(len(xMovement)):
        tempArray = tiltMoveVector(paddyArray, xMovement[i], yMovement[i], xPositionList, yPositionList, nodeList[i])
    print(*paddyArray, sep="\n")
    # 縦の巡回
    # for i in range(vertical):
    #     wall = False
    #     for j in range(beside):
    #         if paddyArray[i][j] == POSITION:
    #             break
    #         if paddyArray[i][j] == WALL:
    #
    #         paddyArray[i][j] = WALL

    return paddyArray


def tiltMoveVector(
        paddyArray, xMovement, yMovement, xPositionList, yPositionList, node
):
    # 傾き
    a = yMovement / xMovement
    # print("傾き", a)
    # print("xPosition", xPositionList[node[0]])
    # print("yPosition", yPositionList[node[0]])
    # print("x軸の移動量", xMovement)
    # print("y軸の移動量", yMovement)
    if xMovement > 0:
        # print(xPositionList[node[0]] + 1, "から", xPositionList[node[1]] + 1, "まで", "+1ずつ")
        for x in range(xPositionList[node[0]] + 1, xPositionList[node[1]] + 1, 1):
            y = a * (xPositionList[node[0]] - x)
            print("yの値", y)
            print("xの値", x)
            y = yPositionList[node[0]] + math.floor(y)
            print("yの値加工後", y)
            print("paddyArray[", y, "][", x, "]を壁とする")
            if paddyArray[y][x] == 0:
                paddyArray[y][x] = WALL
    else:
        # print(xPositionList[node[0]] - 1, "から", xPositionList[node[1]], "まで", "-1ずつ")
        for x in range(xPositionList[node[0]] - 1, xPositionList[node[1]], -1):
            y = a * (xPositionList[node[0]] - x)
            print("yの値", y)
            print("xの値", xPositionList[node[0]] - x)
            y = yPositionList[node[0]] + math.floor(y)
            print("yの値加工後", y)
            print("paddyArray[", y, "][", x, "]を壁とする")
            if paddyArray[y][x] == 0:
                paddyArray[y][x] = WALL
    return paddyArray
