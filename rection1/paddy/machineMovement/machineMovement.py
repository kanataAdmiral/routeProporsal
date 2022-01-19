from rection1.paddy.Repository.moveRepository.move import moveList, moveParameter
from ..Parameters.paddyParameters import movement
from ...util import util


class machineMovement:
    polygonRowList: list
    polygonColumnList: list

    def __init__(self, rowList, columnList):
        self.polygonRowList = rowList
        self.polygonColumnList = columnList

    # 一番最初に呼び出される
    def goStartPosition(self, targetPosition, startPosition, plant, number):
        # 動きのフラグ、Falseならそこが終点
        moveFlag = True

        oneStepMovementList = []
        up = targetPosition[0] - startPosition[0]
        left = targetPosition[1] - startPosition[1]

        now_row_position = startPosition[0]
        now_column_position = startPosition[1]

        # print("行", up, "列", left)
        # print(insideRowList)
        # print(insideColumnList)

        # print("開始", nowRowPosition, nowColumnPosition)
        show_target_position = targetPosition[0] + 1, targetPosition[1] + 1
        print("目標", show_target_position)
        while moveFlag:
            move = movement(up, left, number)
            if now_row_position == targetPosition[0] and now_column_position == targetPosition[1]:
                break
            else:
                number += 1
                vector = move.vector
                string = move.string
                icon = move.icon

                rowVector = -1 * move.vector[0]
                columnVector = -1 * move.vector[1]

                up += rowVector
                left += columnVector

                # 現在のポジションから一つ次のポジションを見る
                next_row_position = now_row_position + move.vector[0]
                next_column_position = now_column_position + move.vector[1]
                # 次のポジションがpolygonの中にあるのかを判定
                in_polygon_flag = util.isPositionInsidePolygon(
                    self.polygonRowList,
                    self.polygonColumnList,
                    next_column_position,
                    next_row_position
                )
                if plant:
                    # 植える、かつ、次のポジションがpolygonの中にあるなら
                    if in_polygon_flag:
                        oneStepMovementList.append(
                            moveParameter(
                                vector,
                                string,
                                icon,
                                number,
                                now_row_position,
                                now_column_position,
                                True
                            )
                        )
                    # 植える、けど、次のポジションがpolygonの中にいないなら
                    # 近くに
                    else:
                        oneStepMovementList.append(
                            moveParameter(
                                vector,
                                string,
                                icon,
                                number,
                                now_row_position,
                                now_column_position,
                                False
                            )
                        )
                else:
                    oneStepMovementList.append(
                        moveParameter(
                            vector,
                            string,
                            icon,
                            number,
                            now_row_position,
                            now_column_position,
                            False
                        )
                    )

                # 現在のポジションを更新
                now_row_position = next_row_position
                now_column_position = next_column_position
        tempMoveList = moveList(tuple(oneStepMovementList))
        return tempMoveList, (now_row_position, now_column_position), number
