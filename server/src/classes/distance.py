from dataclasses import dataclass


@dataclass
class Distance:
    front: float
    back: float
    left: float
    right: float

    def __str__(self):
        return f"front: {self.front}, back: {self.back}, left: {self.left}, right: {self.right}"
