import sys

from ..paddy.Repository.machineRepository import Machine
from ..paddy.machineMovement.machineMovement import machineMovement as m
from ..paddy.Repository.moveRepository.move import movement_list


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
        route_number = 0
        plant = False

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

        print("inside_column_length\n内周横の長さ", inside_column_length)
        print("inside_row_length\n内周縦の長さ", inside_row_length)

        # 縦に向けて検索を開始
        if self.rowFlag:
            print("縦に植える")
            start_position = self.search(inside_row_length, inside_column_length, outside_rs, inside_rs,
                                         start_position, plant, route_number, all_step_movement_list)
        # 横に向けて検索を開始
        else:
            print("横に植える")
            start_position = self.search(inside_column_length, inside_row_length, outside_rs, inside_rs,
                                         start_position, plant, route_number, all_step_movement_list)

        # 外周を描画

        # TODO
        """外周を描画する処理を記述"""

        temp_movement_list = movement_list(
            tuple(all_step_movement_list),
            max(self.outsideCircumferenceRowList),
            max(self.outsideCircumferenceColumnList),
            (self.doorwayColumnList[0], self.doorwayRowList[0])
        )

        return temp_movement_list

    def search(self, one_step_repeat_count, total_step_repeat_count, outside_rs, inside_rs,
               start_position, plant, route_number, all_step_movement_list):
        way_position_list = []
        print("\033[31m" + "出入り口から始点に移動するプログラムを開始" + "\033[0m")
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
        print(target_position)
        inside_rs.search_turning_position(target_position, way_position_list, val_add_flag)
        plant = True
        # 内周を検索
        return self.search_inside(start_position, one_step_repeat_count, total_step_repeat_count,
                                  inside_rs, plant, route_number, all_step_movement_list, way_position_list)

    def search_inside(self, start_position, one_step_repeat_count, total_step_repeat_count,
                      inside_rs, plant, route_number, all_step_movement_list, way_position_list):
        print("\033[31m" + "内周を巡回するときに使われるway_position_listを決める" + "\033[0m")
        # 開始位置のx座標からtotal_step_repeat_count + 1まで繰り返す
        i = 1
        print(start_position)
        print("iのposition", i)
        # one_step_repeat_count を同じ行、または列で繰り返し、旋回のアルゴルズムをまた別で作成する。
        while i <= total_step_repeat_count:
            print("\033[32m" + "iの値", i, "\033[0m")
            val_add_flag = (total_step_repeat_count - i) % 2 == 1
            if self.rowFlag:
                if val_add_flag:
                    target_position = [i, one_step_repeat_count]
                else:
                    target_position = [i, 1]
            else:
                print("i", i)
                if val_add_flag:
                    target_position = [one_step_repeat_count, i]
                else:
                    target_position = [1, i]
            target_position = inside_rs.target_in_polygon(target_position, self.rowFlag, val_add_flag)
            print(target_position)
            way_position_list.append(target_position)
            inside_rs.search_turning_position(target_position, way_position_list, val_add_flag)
            i += 1

        print("\033[31m" + "内周を巡回するプログラムを開始する" + "\033[0m")
        print("way_position_list", *way_position_list, sep="\n")
        count = 0
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
        return start_position


