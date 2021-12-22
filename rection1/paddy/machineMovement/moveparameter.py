from dataclasses import dataclass


@dataclass
class moveParameter:
    vector: tuple[int, int]
    string: str
    icon: str
