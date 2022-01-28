import sys

from rection1.paddy.Repository.moveRepository.move import moveList, move_parameter
from ..Parameters.paddyParameters import movement
from ..util import util


class machineMovement:
    polygonRowList: list
    polygonColumnList: list
    row_flag: bool

    def __init__(self, rowList, columnList, row_flag):
        self.polygonRowList = rowList
        self.polygonColumnList = columnList
        self.row_flag = row_flag

    # 一番最初に呼び出されるx, yの形式で呼び出される
    def search_position(self, target_position, start_position, plant, number):
        # 動きのフラグ、Falseならそこが終点
        moveFlag = True

        oneStepMovementList = []
        left = target_position[0] - start_position[0]
        up = target_position[1] - start_position[1]

        now_column_position = start_position[0]
        now_row_position = start_position[1]

        while moveFlag:
            # movementのflagは上下を優先的に動かすのか、左右を優先的に動かすのかを決定する
            # Trueなら上下、Falseなら左右を優先する
            move = movement(up, left, number, flag=True)
            if now_row_position == target_position[1] and now_column_position == target_position[0]:
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
                next_position_in_polygon = self.is_position_in_polygon(
                    [next_column_position, next_row_position]
                )
                # 今のポジションがpolygonの中にあるのかを判定
                now_position_in_polygon = self.is_position_in_polygon(
                    [now_column_position, now_row_position]
                )

                if plant:
                    # 植える、かつ、次のポジションがpolygonの中にあるなら
                    if next_position_in_polygon:
                        oneStepMovementList.append(
                            move_parameter(
                                vector,
                                string,
                                icon,
                                number,
                                now_row_position,
                                now_column_position,
                                now_position_in_polygon
                            )
                        )
                    # 植える、けど、次のポジションがpolygonの中にいないなら
                    else:
                        oneStepMovementList.append(
                            move_parameter(
                                vector,
                                string,
                                icon,
                                number,
                                now_row_position,
                                now_column_position,
                                now_position_in_polygon
                            )
                        )
                else:
                    oneStepMovementList.append(
                        move_parameter(
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
        now_position = [now_column_position, now_row_position]
        return tempMoveList, now_position, number

    def search_turning_position(self, target_position, way_position_list, val_add_flag):
        # 現在のポジションがターゲットのポジションについたなら旋回するためのターゲットポジションを作成
        # 旋回するためのtargetを生成
        # 縦に進行
        now_x_position = target_position[0]
        now_y_position = target_position[1]
        if self.row_flag:
            # target_positionのy軸が1なら一つ上のポジションをとる必要がある。
            # down_flagがTrueならstart_positionのyの値は小さいものからだんだん大きくなる
            # 上から下に進行する
            next_x_position = now_x_position + 1
            next_y_position = now_y_position
            if val_add_flag:
                while self.is_position_in_polygon([next_x_position, next_y_position]):
                    # 今のpositionから一つ下のpositionをとる
                    next_y_position = next_y_position + 1
                else:
                    new_target_position = [now_x_position, next_y_position]
            # 下から上に進行
            else:
                # 今のpositionが次の列の中にあるならもっと上をとる
                while self.is_position_in_polygon([next_x_position, next_y_position]):
                    # 今のpositionから一つ下のpositionをとる
                    next_y_position = next_y_position - 1
                else:
                    new_target_position = [now_x_position, next_y_position]

            way_position_list.append(new_target_position)
            # 列を変更
            new_target_position = [new_target_position[0] + 1, new_target_position[1]]
            way_position_list.append(new_target_position)
        # 行に向かっている
        # 横に進行
        else:
            # target_positionのx軸の一つ右の軸をとる必要がある
            # down_flagがTrueならstart_positionのxの値は小さいものからだんだん大きくなる
            # 左から右に進行する
            next_x_position = now_x_position
            next_y_position = now_y_position + 1
            if val_add_flag:
                # 今のpositionから一つ右のpositionをとる
                while self.is_position_in_polygon([next_x_position, next_y_position]):
                    # 今のpositionから一つ右のpositionをとる
                    next_x_position = next_x_position + 1
                else:
                    new_target_position = [next_x_position, now_y_position]
            # 右から左に進行する
            else:
                # 今のpositionから一つ左のpositionをとる
                while self.is_position_in_polygon([next_x_position, next_y_position]):
                    # 今のpositionから一つ左のpositionをとる
                    next_x_position = next_x_position - 1
                # 右から左に進行する
                else:
                    new_target_position = [next_x_position, now_y_position]
            way_position_list.append(new_target_position)
            # 列を変更
            new_target_position = [new_target_position[0], new_target_position[1] + 1]
            way_position_list.append(new_target_position)

    def is_position_in_polygon(self, position):
        return util.is_position_inside_polygon(
            self.polygonRowList,
            self.polygonColumnList,
            position
        )

    # targetの座標がpolygonの中になかった時に呼び出され
    # 新しいtargetを生成する
    def target_in_polygon(self, target_position, row_flag, val_add_flag):
        now_x_position = target_position[0]
        now_y_position = target_position[1]
        if row_flag:
            next_x_position = now_x_position
            next_y_position = now_y_position
            while not self.is_position_in_polygon([next_x_position, next_y_position]):
                if val_add_flag:
                    next_y_position -= 1
                else:
                    next_y_position += 1
            else:
                target_position = [now_x_position, next_y_position]
        else:
            next_x_position = now_x_position
            next_y_position = now_y_position
            while not self.is_position_in_polygon([next_x_position, next_y_position]):
                if val_add_flag:
                    next_x_position -= 1
                else:
                    next_x_position += 1
            else:
                target_position = [next_x_position, now_y_position]
        return target_position

    # 最初のtargetの座標を作成
    # target_positionは y, x
    # 一つ隣の列、行を参照して、その行に合わせたtarget_positionを特定する
    def re_target_position(self, target_position, row_flag, val_add_flag):
        # 縦に進行
        now_x_position = target_position[0]
        now_y_position = target_position[1]
        if row_flag:
            next_x_position = now_x_position + 1
            next_y_position = now_y_position
            # もしtargetがpolygonの中にいないなら
            # 座標をpolygonの中になるように変更する。現在のx座標と、更新されたy座標を変更する
            while not self.is_position_in_polygon([next_x_position, next_y_position]):
                if val_add_flag:
                    next_y_position -= 1
                else:
                    next_y_position += 1
            else:
                target_position = [now_x_position, next_y_position]
        # 横に進行
        else:
            # 一つ下の軸のpositionを参照する
            next_x_position = now_x_position
            next_y_position = now_y_position + 1
            # もしtargetがpolygonの中にいないなら
            # 座標をpolygonの中になるように変更する。現在のx座標と、更新されたy座標を渡す
            while not self.is_position_in_polygon([next_x_position, next_y_position]):
                if val_add_flag:
                    next_x_position -= 1
                else:
                    next_x_position += 1
            else:
                target_position = [next_x_position, now_y_position]
        return target_position
