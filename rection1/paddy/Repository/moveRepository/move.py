from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class moveParameter:
    vector: tuple[int, int]
    string: str
    icon: str
    number: int
    rowPosition: int
    columnPosition: int
    plant: bool


@dataclass_json
@dataclass
class moveList:
    stepMoveList: tuple[moveParameter]


@dataclass_json
@dataclass
class movementList:
    AllMoveList: tuple[moveList]
    maxRow: int
    maxColumn: int
