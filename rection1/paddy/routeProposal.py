from ..paddy.Repository.machineRepository import Machine
from ..paddy.machineMovement.machineMovement import machineMovement as m
from ..paddy.Repository.moveRepository.move import movementList


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

    def searchRoute(self):
        AllStepMovementList = []
        routeNumber = 0
        plant = False

        doorwayList = (self.doorwayRowList[0], self.doorwayColumnList[0])

        insideColumnLength = max(self.insideColumnList) - min(self.insideColumnList) + 1
        insideRowLength = max(self.insideRowList) - min(self.insideRowList) + 1

        outSideColumnLength = max(self.outsideCircumferenceColumnList) - self.outsideCircumferenceColumnList[0] + 1
        outSideRowLength = max(self.outsideCircumferenceRowList) - self.outsideCircumferenceRowList[0] + 1

        print(self.outsideCircumferenceRowList)
        print(self.outsideCircumferenceColumnList)
        print()
        print(self.insideRowList)
        print(self.insideColumnList)

        outsideRS = m(rowList=self.outsideCircumferenceRowList, columnList=self.outsideCircumferenceColumnList)
        insideRS = m(rowList=self.insideRowList, columnList=self.insideColumnList)

        startPosition = self.search(insideRowLength, insideColumnLength, outsideRS, insideRS,
                                    doorwayList, plant, routeNumber, AllStepMovementList)

        # 外周を描画
        print("現在のポジションを表示", startPosition)

        # TODO
        """外周を描画する処理を記述"""

        tempMovementList = movementList(
            tuple(AllStepMovementList),
            max(self.outsideCircumferenceRowList),
            max(self.outsideCircumferenceColumnList)
        )
        # print(tempMovementList)
        # print(tempMovementList.to_json(indent=4, ensure_ascii=False))

        return tempMovementList

    def search(self, insideRowLength, insideColumnLength, outsideRS, insideRS,
               doorwayList, plant, routeNumber, AllStepMovementList):
        # 出入り口が各ポジションのどこに近いのかを見つける
        print("出入り口からスタートラインに行く")
        if insideColumnLength % 2 == 0:
            # print("偶数")
            # 田んぼの内周が偶数ならまずは下に向かう
            # 最も左上のポジションを取得
            leftTopPosition = self.insideRowList[0], self.insideColumnList[0]
            oneStepMovementList, startPosition, routeNumber = outsideRS.goStartPosition(
                leftTopPosition,
                doorwayList,
                plant,
                routeNumber
            )
            AllStepMovementList.append(oneStepMovementList)
            plant = True
            # 内周を検索
            return search_inside_even(startPosition, insideColumnLength, insideRowLength,
                                      insideRS, plant, routeNumber, AllStepMovementList)
        else:
            # 内周を進行する
            # 0が行, 1が列
            # print(startPosition[1])
            # 列を回す
            # print("奇数")
            # 田んぼの内周が奇数ならまずは上に向かう
            # 最も左下のポジションを取得
            leftBottomPosition = self.insideRowList[0], self.insideColumnList[0]
            oneStepMovementList, startPosition, routeNumber = outsideRS.goStartPosition(
                leftBottomPosition,
                doorwayList,
                plant,
                routeNumber
            )
            AllStepMovementList.append(oneStepMovementList)
            plant = True

            # 内周を検索
            return search_inside_odd(startPosition, insideColumnLength, insideRowLength,
                                     insideRS, plant, routeNumber, AllStepMovementList)


def search_inside_even(startPosition, insideColumnLength, insideRowLength,
                       insideRS, plant, routeNumber, AllStepMovementList):
    print("現在の内周は偶数だったため今から下に向かってルート検索を開始する")
    for i in range(startPosition[1], insideColumnLength):
        # print("i", i)
        # print(insideColumnLength, "-", i, "=", insideColumnLength - i)
        # print("nowColumnPosition", i)
        # print("doorwayList", doorwayList)
        # print("leftTopPosition", leftTopPosition)
        # print("i", i)
        if (insideColumnLength - i) % 2 == 0:
            # print("偶数")
            targetPosition = insideRowLength, i
            # print("targetPosition", targetPosition)
            oneStepMovementList, startPosition, routeNumber = insideRS.goStartPosition(
                targetPosition,
                startPosition,
                plant,
                routeNumber
            )
            # print("現在の位置", startPosition)
        else:
            # print("奇数")
            targetPosition = 1, i
            # print("targetPosition", targetPosition)
            oneStepMovementList, startPosition, routeNumber = insideRS.goStartPosition(
                targetPosition,
                startPosition,
                plant,
                routeNumber
            )
            # print("現在の位置", startPosition)
        AllStepMovementList.append(oneStepMovementList)
    return startPosition


def search_inside_odd(startPosition, insideColumnLength, insideRowLength,
                      insideRS, plant, routeNumber, AllStepMovementList):
    print("現在の内周は奇数だったため今から上に向かってルート検索を開始する")
    for i in range(startPosition[1], insideColumnLength):
        print("i", i)
        # print(insideColumnLength, "-", i, "=", insideColumnLength - i)
        # print("nowColumnPosition", i)
        # print("doorwayList", doorwayList)
        # print("leftTopPosition", leftTopPosition)
        # print("i", i)
        if (insideColumnLength - i) % 2 == 0:
            # print("偶数")
            targetPosition = insideRowLength, i
            # print("targetPosition", targetPosition)
            oneStepMovementList, startPosition, routeNumber = insideRS.goStartPosition(
                targetPosition,
                startPosition,
                plant,
                routeNumber
            )
            # print("現在の位置", startPosition)
        else:
            # print("奇数")
            targetPosition = 1, i
            # print("targetPosition", targetPosition)
            oneStepMovementList, startPosition, routeNumber = insideRS.goStartPosition(
                targetPosition,
                startPosition,
                plant,
                routeNumber
            )
            # print("現在の位置", startPosition)
        AllStepMovementList.append(oneStepMovementList)
    return startPosition
