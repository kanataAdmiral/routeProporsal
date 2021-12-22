from rection1.paddy.Model.machineModel import Machine
from ..paddy.machineMovement import machineMovement as m


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

    movementList: list

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
        movementList = []
        for i in range(len(self.outsideCircumferenceRowList)):
            outsideList.append((self.outsideCircumferenceRowList[i], self.outsideCircumferenceColumnList[i]))
        for i in range(len(self.insideRowList)):
            insideList.append((self.insideRowList[i], self.insideColumnList[i]))

        doorwayList = (self.doorwayRowList[0], self.doorwayColumnList[0])
        insideColumnLength = max(self.insideColumnList) - self.insideColumnList[0]
        insideRowLength = max(self.insideRowList) - self.insideRowList[0]

        print(insideColumnLength)
        print(insideRowLength)

        # 出入り口が各ポジションのどこに近いのかを見つける
        if insideColumnLength % 2 == 0:
            print("偶数")
            # 田んぼの内周が偶数ならまずは下に向かう
            # 最も左上のポジションを取得
            leftTopPosition = self.insideRowList[0], self.insideColumnList[0]
            moveList, startPosition = m.goStartPosition(leftTopPosition,
                                                        doorwayList,
                                                        self.outsideCircumferenceRowList,
                                                        self.outsideCircumferenceColumnList)
            movementList.append(moveList)
            # 0が行, 1が列
            print(startPosition[1])
            # 列を回す
            nowRowPosition = startPosition[0]
            nowColumnPosition = startPosition[1]
            for i in range(startPosition[1], insideColumnLength + 1):
                if (insideColumnLength - nowColumnPosition) % 2 == 0:
                    print("偶数")
                else:
                    print("奇数")

        else:
            print("奇数")
            # 田んぼの内周が奇数ならまず上に向かう
            # 最も左下のポジションを取得
            leftTopPosition = insideRowLength, self.insideColumnList[0]
            moveList, startPosition = m.goStartPosition(leftTopPosition,
                                                        doorwayList,
                                                        self.outsideCircumferenceRowList,
                                                        self.outsideCircumferenceColumnList)
            movementList.append(moveList)

            nowRowPosition = startPosition[0]
            nowColumnPosition = startPosition[1]
            for i in range(startPosition[0], insideColumnLength + 1):
                if (insideColumnLength - nowColumnPosition) % 2 == 0:
                    print("偶数")
                else:
                    print("奇数")
