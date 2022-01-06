from ..machineMovement.moveparameter import moveList, moveParameter
from ..Parameters.paddyParameters import movement
from ...util import util


# 一番最初に呼び出される
def goStartPosition(targetPosition, startPosition, insideRowList, insideColumnList):
    # 動きのフラグ、Falseならそこが終点
    moveFlag = True

    oneStepMovementList = []

    # 上なら負, 下なら正, 上下しないなら0
    up = targetPosition[0] - startPosition[0]
    # 左なら負, 右なら正, 左右しないなら0
    left = targetPosition[1] - startPosition[1]

    nowRowPosition = startPosition[0]
    nowColumnPosition = startPosition[1]

    print("行", up, "列", left)

    while moveFlag:
        move = movement(up, left)
        print("現在の行", nowRowPosition, "列", nowColumnPosition)
        print("目標の行", targetPosition[0], "列", targetPosition[1])
        if nowRowPosition == targetPosition[0] and nowColumnPosition == targetPosition[1]:
            moveFlag = False
            print("目標到達")
        else:
            vector = move.vector
            string = move.string
            icon = move.icon

            rowVector = -1 * move.vector[0]
            columnVector = -1 * move.vector[1]

            up += rowVector
            left += columnVector

            nowRowPosition += move.vector[0]
            nowColumnPosition += move.vector[1]

            if util.isPositionInsidePolygon(insideRowList, insideColumnList, nowColumnPosition, nowRowPosition):
                oneStepMovementList.append(moveParameter(vector, string, icon))
            else:
                print("polygonの中ではなくなった")
                pass
            print("中身を表示")
            for i in oneStepMovementList:
                print(i.vector)
                print(i.icon)
                print(i.string)
    tempMoveList = moveList(oneStepMovementList)
    return tempMoveList, (nowRowPosition, nowColumnPosition)




