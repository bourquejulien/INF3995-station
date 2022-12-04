from dataclasses import dataclass

FLOATING_PRECISION = 2


@dataclass
class Position:
    x: float
    y: float
    z: float

    def __str__(self):
        return f"x: {round(self.x, FLOATING_PRECISION)}, y: {round(self.y, FLOATING_PRECISION)}, z: {round(self.z, FLOATING_PRECISION)}"

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, other):
        return Position(self.x * other, self.y * other, self.z * other)
