from dataclasses import dataclass


@dataclass
class Position:
    x: float
    y: float
    z: float

    def __str__(self):
        return f"x{self.x}, y: {self.y}, z: {self.z}"
