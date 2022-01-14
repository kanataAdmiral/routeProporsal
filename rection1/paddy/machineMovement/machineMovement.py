from rection1.paddy.Repository.moveRepository.move import moveList, moveParameter
from ..Parameters.paddyParameters import movement
from ...util import util


# 一番最初に呼び出される
def goStartPosition(targetPosition, startPosition, insideRowList, insideColumnList, plant):
    # 動きのフラグ、Falseならそこが終点
    moveFlag = True

    oneStepMovementList = []
    up = targetPosition[0] - startPosition[0]
    left = targetPosition[1] - startPosition[1]

    nowRowPosition = startPosition[0]
    nowColumnPosition = startPosition[1]

    # print("行", up, "列", left)
    # print(insideRowList)
    # print(insideColumnList)

    # print("開始", nowRowPosition, nowColumnPosition)
    # print("目標", targetPosition)
    while moveFlag:
        move = movement(up, left)
        if nowRowPosition == targetPosition[0] and nowColumnPosition == targetPosition[1]:
            # print("目標到達")
            moveFlag = False
        else:
            vector = move.vector
            string = move.string
            icon = move.icon

            rowVector = -1 * move.vector[0]
            columnVector = -1 * move.vector[1]

            up += rowVector
            left += columnVector
            # print(nowRowPosition, ",", nowColumnPosition, "はポリゴンの中にある")
            oneStepMovementList.append(
                moveParameter(
                    vector,
                    string,
                    icon,
                    nowRowPosition,
                    nowColumnPosition,
                    util.isPositionInsidePolygon(
                        insideRowList,
                        insideColumnList,
                        nowColumnPosition,
                        nowRowPosition
                    ) and plant
                )
            )

            nowRowPosition += move.vector[0]
            nowColumnPosition += move.vector[1]
    tempMoveList = moveList(tuple(oneStepMovementList))
    return tempMoveList, (nowRowPosition, nowColumnPosition)
