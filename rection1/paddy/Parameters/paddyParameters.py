START_POSITION = "S"
END_POSITION = "E"
OUTSIDE_POSITION = "P"
INSIDE_POSITION = "I"


class movement:
    vector: tuple
    string: str
    icon: str
    number: int

    def __init__(self, up, left, number, flag=True):
        self.number = number
        # 上なら負, 下なら正, 上下しないなら0
        # 左なら負, 右なら正, 左右しないなら0
        if flag:
            if up < 0:
                self.vector = -1, 0
                self.string = "上"
                self.icon = "↑"
            elif up > 0:
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
        else:
            # 左なら負, 右なら正, 左右しないなら0
            # 上なら負, 下なら正, 上下しないなら0
            if left < 0:
                self.vector = 0, -1
                self.string = "左"
                self.icon = "←"
            elif left > 0:
                self.vector = 0, 1
                self.string = "右"
                self.icon = "→"
            else:
                if up < 0:
                    self.vector = -1, 0
                    self.string = "上"
                    self.icon = "↑"
                elif up > 0:
                    self.vector = 1, 0
                    self.string = "下"
                    self.icon = "↓"
                else:
                    self.vector = 0, 0
                    self.string = "終点"
                    self.icon = "・"
