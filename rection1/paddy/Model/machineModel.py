from dataclasses import dataclass

JOUKAN = 30
KABUMA = 18


@dataclass
class Machine:
    # 機械の幅
    width: int
    # 機械の長さ
    length: int
    # 何条植えなのかを格納
    plant: int
    # 条間
    BetweenTheLines: int
    # 株間
    BetweenStocks: int

    def __init__(self, plant, width, length, joukan=JOUKAN, kabuma=KABUMA):
        self.plant = plant
        self.width = width
        self.length = length
        # 条間
        self.BetweenTheLines = joukan * plant
        # 株間
        self.BetweenStocks = kabuma
