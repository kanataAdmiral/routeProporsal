from rection1.paddy.machineMovement.moveparameter import *

START_POSITION = "S"
END_POSITION = "E"
OUTSIDE_POSITION = "P"
INSIDE_POSITION = "I"


class movement:
    vector: tuple
    string: str
    icon: str

    def __init__(self, up, left):
        if up < 0:
            if left < 0:
                # 左上
                self.vector = -1, -1
                self.string = "上左"
                self.icon = "↖"
            elif left > 0:
                # 右上
                self.vector = -1, 1
                self.string = "上右"
                self.icon = "↗"
            else:
                # 上
                self.vector = -1, 0
                self.string = "上"
                self.icon = "↑"
        elif up > 0:
            if left < 0:
                self.vector = 1, -1
                self.string = "下左"
                self.icon = "↙"
            elif left > 0:
                self.vector = 1, 1
                self.string = "下右"
                self.icon = "↘"
            else:
                self.vector = 1, 0
                self.string = "下"
                self.icon = "↓"
        else:
            if left < 0:
                self.vector = 0, -1
                self.string = "左"
                self.icon = "←"
            elif left > 0:
                self.vector = 0, 1
                self.string = "右"
                self.icon = "→"
            else:
                self.vector = 0, 0
                self.string = "終点"
                self.icon = "・"
