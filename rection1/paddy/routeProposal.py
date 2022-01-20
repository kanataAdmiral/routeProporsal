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

        start_position = (self.doorwayRowList[0], self.doorwayColumnList[0])

        inside_column_length = max(self.insideColumnList) - min(self.insideColumnList) + 1
        inside_row_length = max(self.insideRowList) - min(self.insideRowList) + 1

        outSideColumnLength = max(self.outsideCircumferenceColumnList) - self.outsideCircumferenceColumnList[0] + 1
        outSideRowLength = max(self.outsideCircumferenceRowList) - self.outsideCircumferenceRowList[0] + 1

        print("inside_column_length\n内周列の長さ", inside_column_length)
        print("inside_row_length\n内周行の長さ", inside_row_length)

        outside_rs = m(rowList=self.outsideCircumferenceRowList, columnList=self.outsideCircumferenceColumnList)
        inside_rs = m(rowList=self.insideRowList, columnList=self.insideColumnList)
        print("insideRowList", self.insideRowList)
        print("insideColumnList", self.insideColumnList)

        # 縦に向けて検索を開始
        if self.rowFlag:
            start_position = self.search(inside_row_length, inside_column_length, outside_rs, inside_rs,
                                         start_position, plant, route_number, all_step_movement_list)
        # 横に向けて検索を開始
        else:
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

    def search(self, start, search, outside_rs, insideRS,
               start_position, plant, route_number, all_step_movement_list):
        # 出入り口が各ポジションのどこに近いのかを見つける
        if search % 2 == 0:
            target_position = self.insideRowList[0], self.insideColumnList[0]
        else:
            target_position = search, self.insideColumnList[0]

        one_step_movement_list, start_position, route_number = outside_rs.search_position(
            target_position,
            start_position,
            plant,
            route_number
        )
        all_step_movement_list.append(one_step_movement_list)
        plant = True

        # 内周を検索
        return self.search_inside(start_position, search, start,
                                  insideRS, plant, route_number, all_step_movement_list)

    def search_inside(self, start_position, search, start,
                      inside_rs, plant, route_number, all_step_movement_list):
        for i in range(start_position[1], search + 1):
            if (search - i) % 2 == 0:
                if self.rowFlag:
                    target_position = start, i
                else:
                    target_position = i, start
                one_step_movement_list, start_position, route_number = inside_rs.search_position(
                    target_position,
                    start_position,
                    plant,
                    route_number
                )
            else:
                if self.rowFlag:
                    target_position = 1, i
                else:
                    target_position = i, 1
                one_step_movement_list, start_position, route_number = inside_rs.search_position(
                    target_position,
                    start_position,
                    plant,
                    route_number
                )
            all_step_movement_list.append(one_step_movement_list)
        return start_position

# def find_target_position(target_row, target_column, polygon):
#     if polygon.is_position_in_polygon(target_column, target_row):
