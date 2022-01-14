from rection1.paddy.Repository.machineRepository import Machine
from ..paddy.machineMovement import machineMovement as m
from rection1.paddy.Repository.moveRepository.move import movementList


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
                 machineInfo
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

    def searchRoute(self):
        outsideList = []
        insideList = []
        AllStepMovementList = []
        routeNumber = 1
        plant = False

        for i in range(len(self.outsideCircumferenceRowList)):
            outsideList.append((self.outsideCircumferenceRowList[i], self.outsideCircumferenceColumnList[i]))
        for i in range(len(self.insideRowList)):
            insideList.append((self.insideRowList[i], self.insideColumnList[i]))

        doorwayList = (self.doorwayRowList[0], self.doorwayColumnList[0])

        insideColumnLength = max(self.insideColumnList) - self.insideColumnList[0] + 1
        insideRowLength = max(self.insideRowList) - self.insideRowList[0] + 1

        outSideColumnLength = max(self.outsideCircumferenceColumnList) - self.outsideCircumferenceColumnList[0] + 1
        outSideRowLength = max(self.outsideCircumferenceRowList) - self.outsideCircumferenceRowList[0] + 1

        rowList = self.insideRowList
        columnList = self.insideColumnList

        rowList.sort()
        columnList.sort()

        # 出入り口が各ポジションのどこに近いのかを見つける
        if insideColumnLength % 2 == 0:
            # print("偶数")
            # 田んぼの内周が偶数ならまずは下に向かう
            # 最も左上のポジションを取得
            leftTopPosition = self.insideRowList[0], self.insideColumnList[0]
            oneStepMovementList, startPosition = m.goStartPosition(
                leftTopPosition,
                doorwayList,
                self.outsideCircumferenceRowList,
                self.outsideCircumferenceColumnList,
                plant
            )
            AllStepMovementList.append(oneStepMovementList)

            # 内周を進行する
            # 0が行, 1が列
            # print(startPosition[1])
            # 列を回す
            plant = True
            print("外周の列の長さ", outSideColumnLength)
            print("内周の列の長さ", insideColumnLength)
            print("range", range(startPosition[1], outSideColumnLength - 1))
            for i in range(startPosition[1], outSideColumnLength - 1):
                routeNumber += 1
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
                    oneStepMovementList, startPosition = m.goStartPosition(
                        targetPosition,
                        startPosition,
                        self.outsideCircumferenceRowList,
                        self.outsideCircumferenceColumnList,
                        plant
                    )
                    # print("現在の位置", startPosition)
                else:
                    # print("奇数")
                    targetPosition = 1, i
                    # print("targetPosition", targetPosition)
                    oneStepMovementList, startPosition = m.goStartPosition(
                        targetPosition,
                        startPosition,
                        self.outsideCircumferenceRowList,
                        self.outsideCircumferenceColumnList,
                        plant
                    )
                    # print("現在の位置", startPosition)
                AllStepMovementList.append(oneStepMovementList)
            insideRouteOverPosition = startPosition
            print(insideRouteOverPosition)
        else:
            # print("奇数")
            # 田んぼの内周が奇数ならまずは上に向かう
            # 最も左下のポジションを取得
            leftBottomPosition = self.insideRowList[0], self.insideColumnList[0]
            oneStepMovementList, startPosition = m.goStartPosition(
                leftBottomPosition,
                doorwayList,
                self.outsideCircumferenceRowList,
                self.outsideCircumferenceColumnList,
                plant
            )
            AllStepMovementList.append(oneStepMovementList)
            plant = True
            print("外周の列の長さ", outSideColumnLength)
            print("内周の列の長さ", insideColumnLength)
            print("range", range(startPosition[1], outSideColumnLength - 1))
            for i in range(startPosition[1], outSideColumnLength - 1):
                routeNumber += 1
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
                    oneStepMovementList, startPosition = m.goStartPosition(
                        targetPosition,
                        startPosition,
                        self.outsideCircumferenceRowList,
                        self.outsideCircumferenceColumnList,
                        plant
                    )
                    # print("現在の位置", startPosition)
                else:
                    # print("奇数")
                    targetPosition = 1, i
                    # print("targetPosition", targetPosition)
                    oneStepMovementList, startPosition = m.goStartPosition(
                        targetPosition,
                        startPosition,
                        self.outsideCircumferenceRowList,
                        self.outsideCircumferenceColumnList,
                        plant
                    )
                    # print("現在の位置", startPosition)
                AllStepMovementList.append(oneStepMovementList)
            insideRouteOverPosition = startPosition
            print(insideRouteOverPosition)

        # 外周を描画
        print("現在のポジションを表示", startPosition)
        tempMovementList = movementList(
            tuple(AllStepMovementList),
            max(self.outsideCircumferenceRowList),
            max(self.outsideCircumferenceColumnList)
        )
        # print(tempMovementList)
        # print(tempMovementList.to_json(indent=4, ensure_ascii=False))

        return tempMovementList
