from ..Parameters.paddyParameters import movement as mv
from ...util import util


# 一番最初に呼び出される
def goStartPosition(leftTopPosition, startPosition, insideRowList, insideColumnList):
    # 動きのフラグ、Falseならそこが終点
    moveFlag = True

    movementList = []

    # 上なら負, 下なら正, 上下しないなら0
    up = leftTopPosition[0] - startPosition[0]
    # 左なら負, 右なら正, 左右しないなら0
    left = leftTopPosition[1] - startPosition[1]

    nowRowPosition = startPosition[0]
    nowColumnPosition = startPosition[1]

    print("行", up, "列", left)

    while moveFlag:
        print("現在の行", nowRowPosition, "列", nowColumnPosition)
        print("目標の行", leftTopPosition[0], "列", leftTopPosition[1])
        if nowRowPosition == leftTopPosition[0] and nowColumnPosition == leftTopPosition[1]:
            moveFlag = False
            print("目標到達")
        else:
            move = mv(up, left).move
            rowVector = -1 * move.vector[0]
            columnVector = -1 * move.vector[1]
            up += rowVector
            left += columnVector
            nowRowPosition += move.vector[0]
            nowColumnPosition += move.vector[1]
            if util.isPositionInsidePolygon(insideRowList, insideColumnList, nowColumnPosition, nowRowPosition):
                movementList.append(move)
            else:
                print("polygonの中ではなくなった")
                pass
    return movementList, (nowRowPosition, nowColumnPosition)
