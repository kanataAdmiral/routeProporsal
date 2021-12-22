
from ..machineMovement.moveparameter import *

START_POSITION = "S"
END_POSITION = "E"
OUTSIDE_POSITION = "P"
INSIDE_POSITION = "I"


class movement:
    move = None
    def __init__(self, up, left):
        move = moveParameter
        if up < 0:
            if left < 0:
                # 左上
                move.vector = -1, -1
                move.string = "上左"
                move.icon = "↖"
            elif left > 0:
                # 右上
                move.vector = -1, 1
                move.string = "上右"
                move.icon = "↗"
            else:
                # 上
                move.vector = -1, 0
                move.string = "上"
                move.icon = "↑"
        elif up > 0:
            if left < 0:
                move.vector = 1, -1
                move.string = "下左"
                move.icon = "↙"
            elif left > 0:
                move.vector = 1, 1
                move.string = "下右"
                move.icon = "↘"
            else:
                move.vector = 1, 0
                move.string = "下"
                move.icon = "↓"
        else:
            if left < 0:
                move.vector = 0, -1
                move.string = "左"
                move.icon = "←"
            elif left > 0:
                move.vector = 0, 1
                move.string = "右"
                move.icon = "→"
            else:
                move.vector = 0, 0
                move.string = "終点"
                move.icon = "・"
        self.move = move
        print(move.vector)
        print(move.string)
        print(move.icon)
