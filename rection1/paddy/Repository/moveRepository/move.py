from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class move_parameter:
    vector: tuple[int, int]
    string: str
    icon: str
    number: int
    row_position: int
    column_position: int
    plant: bool


@dataclass_json
@dataclass
class moveList:
    step_move_list: tuple[move_parameter]


@dataclass_json
@dataclass
class movement_list:
    all_move_list: tuple[moveList]
    max_row: int
    max_column: int
    door_way_list: tuple
