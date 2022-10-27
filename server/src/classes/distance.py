from dataclasses import dataclass


@dataclass
class Distance:
    front: float
    back: float
    left: float
    right: float
    up: float
    down: float
