from ..paddy.Repository.machineRepository import Machine
from ..paddy.machineMovement.machineMovement import machineMovement as m
from ..paddy.Repository.moveRepository.move import movement_list
from .util import util


def fill_inside_route_to_json(inside_rs, way_position_list, all_step_movement_list, start_position):
    route_number = 1
    count = 0
    last_target_position = start_position
    for target_position in way_position_list:
        if count == 0:
            plant = False
        else:
            plant = True
        one_step_movement_list, start_position, route_number = inside_rs.search_position(
            target_position,
            start_position,
            plant,
            route_number
        )
        all_step_movement_list.append(one_step_movement_list)
        count += 1

    return all_step_movement_list, start_position


def fill_outside_route_to_json(inside_rs, outside_way_position_list, all_step_movement_list, start_position):
    for outside_target_position, plant_flag in outside_way_position_list:
        if plant_flag:
            print("植える")
        else:
            print("植えない")
    return all_step_movement_list


class RouteProposal:
    paddyArray: list[list[any]]

    outsideRowList: list[int]
    outsideColumnList: list[int]

    insideRowList: list[int]
    insideColumnList: list[int]

    doorwayColumnList: list[int]
    doorwayRowList: list[int]

    inside: list
    outside: list[list]

    machineInfo: Machine

    rowFlag: bool

    target_position_list: list = []

    def __init__(self,
                 paddyArray,
                 outsideRowList,
                 outsideColumnList,
                 insideRowList,
                 insideColumnList,
                 doorwayRowList,
                 doorwayColumnList,
                 outside,
                 inside,
                 machineInfo,
                 rowFlag
                 ):
        self.paddyArray = paddyArray
        self.outsideCircumferenceRowList = outsideRowList
        self.outsideCircumferenceColumnList = outsideColumnList
        self.insideRowList = insideRowList
        self.insideColumnList = insideColumnList
        self.doorwayColumnList = doorwayColumnList
        self.doorwayRowList = doorwayRowList
        self.outside = outside
        self.inside = inside
        self.machineInfo = machineInfo
        self.rowFlag = rowFlag

    def search_route(self):
        # 必要な変数を定義
        all_step_movement_list = []
        way_position_list = []
        outside_way_position_list = []

        start_position = (self.doorwayColumnList[0], self.doorwayRowList[0])

        inside_column_length = max(self.insideColumnList) - min(self.insideColumnList) + 1
        inside_row_length = max(self.insideRowList) - min(self.insideRowList) + 1

        outSideColumnLength = max(self.outsideCircumferenceColumnList) - self.outsideCircumferenceColumnList[0] + 1
        outSideRowLength = max(self.outsideCircumferenceRowList) - self.outsideCircumferenceRowList[0] + 1

        outside_rs = m(rowList=self.outsideCircumferenceRowList,
                       columnList=self.outsideCircumferenceColumnList,
                       row_flag=self.rowFlag)
        inside_rs = m(rowList=self.insideRowList,
                      columnList=self.insideColumnList,
                      row_flag=self.rowFlag)

        # 縦に向けて検索を開始
        if self.rowFlag:
            way_position_list = self.search_inside_route(inside_row_length, inside_column_length,
                                                         inside_rs, way_position_list)
        # 横に向けて検索を開始
        else:
            way_position_list = self.search_inside_route(inside_column_length, inside_row_length,
                                                         inside_rs, way_position_list)

        # 外周を描画

        all_step_movement_list, start_position = fill_inside_route_to_json(inside_rs, way_position_list,
                                                                           all_step_movement_list, start_position)

        outside_way_position_list = self.search_outside_route(start_position, outside_way_position_list)

        # all_step_movement_list = fill_outside_route_to_json(inside_rs, outside_way_position_list,
        #                                                     all_step_movement_list, start_position)

        temp_movement_list = movement_list(
            tuple(all_step_movement_list),
            max(self.outsideCircumferenceRowList),
            max(self.outsideCircumferenceColumnList),
            (self.doorwayColumnList[0], self.doorwayRowList[0])
        )

        return temp_movement_list

    def search_inside_route(self, one_step_repeat_count, total_step_repeat_count, inside_rs,
                            way_position_list):

        # 田んぼの内周を機械が通るとき偶数回、奇数回なのかを判定
        # 実際はそれにはよらない可能性が高い 仮置き
        # 縦、横のどちらかで回転を行っているため、それに従って座標を変更
        if self.rowFlag:
            # 縦に進行する
            if total_step_repeat_count % 2 == 0:
                # 偶数なら
                # x, yで作成
                target_position = [0, self.insideRowList[0]]
                val_add_flag = False
            else:
                # 奇数なら
                target_position = [0, one_step_repeat_count]
                val_add_flag = True
        else:
            # 横に進行する
            if total_step_repeat_count % 2 == 0:
                # 偶数なら
                # x, yで作成
                target_position = [self.insideColumnList[0], 0]
                val_add_flag = False
            else:
                # 奇数なら
                target_position = [one_step_repeat_count, 0]
                val_add_flag = True

        target_position = inside_rs.re_target_position(target_position, self.rowFlag, val_add_flag)
        way_position_list.append(target_position)

        first, second = inside_rs.search_turning_position(target_position, val_add_flag)

        way_position_list.append(first)
        way_position_list.append(second)
        # 内周を検索
        return self.search_inside(one_step_repeat_count, total_step_repeat_count,
                                  inside_rs, way_position_list)

    def search_inside(self, one_step_repeat_count, total_step_repeat_count,
                      inside_rs, way_position_list):
        # 開始位置のx座標からtotal_step_repeat_count + 1まで繰り返す
        i = 1
        # one_step_repeat_count を同じ行、または列で繰り返し、旋回のアルゴルズムをまた別で作成する。
        while i <= total_step_repeat_count:
            val_add_flag = (total_step_repeat_count - i) % 2 == 1
            if self.rowFlag:
                if val_add_flag:
                    target_position = [i, one_step_repeat_count]
                else:
                    target_position = [i, 1]
            else:
                if val_add_flag:
                    target_position = [one_step_repeat_count, i]
                else:
                    target_position = [1, i]
            target_position = inside_rs.target_in_polygon(target_position, self.rowFlag, val_add_flag)
            way_position_list.append(target_position)
            first, second = inside_rs.search_turning_position(target_position, val_add_flag)
            way_position_list.append(first)
            way_position_list.append(second)
            i += 1

        return way_position_list

    def search_outside_route(self, now_position, outside_way_position_list):
        print("\033[31m" + "外周のターゲットポジションを決定するプログラムを開始する" + "\033[0m")
        outside_list = []
        move_list = []
        door_way_position = (self.doorwayColumnList[0], self.doorwayRowList[0])
        for i in range(len(self.outsideCircumferenceRowList)):
            outside_list.append([self.outsideCircumferenceColumnList[i], self.outsideCircumferenceRowList[i]])

        # 現在のポジションから内周の各ポジションのどれに近いのかを算出
        now_most_close_index = util.most_close_index(now_position, outside_list)
        door_way_most_close_index = util.most_close_index(door_way_position, outside_list)

        print("most_close_index", now_most_close_index)
        print("door_way_most_close_index", door_way_most_close_index)
        # まずは出入り口へ進行する
        if now_most_close_index > door_way_most_close_index:
            for i in range(now_most_close_index, door_way_most_close_index, -1):
                move_list.append(i)

        else:
            for i in range(now_most_close_index, door_way_most_close_index):
                move_list.append(i)

        move_list.append(door_way_most_close_index)

        outside_way_position_list.append([outside_list[now_most_close_index], False])

        for move_index in range(1, len(move_list)):
            now_position = outside_list[move_list[move_index - 1]]
            next_position = outside_list[move_list[move_index]]

            print(util.position_to_position_distance(now_position, door_way_position, next_position))

        return outside_way_position_list
