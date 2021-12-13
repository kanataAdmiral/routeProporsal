from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Paddy:
    position: int = None
    x: float = None
    y: float = None


@dataclass_json
@dataclass
class PaddyParameter:
    paddyFields: list[Paddy] = field(default_factory=list)


@dataclass_json
@dataclass
class Position:
    position: int = None
    x: float = None
    y: float = None


@dataclass_json
@dataclass
class StartEndPosition:
    StartEndPosition: list[Position] = field(default_factory=list)
