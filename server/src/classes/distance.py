from dataclasses import dataclass

FLOATING_PRECISION = 2


@dataclass
class Distance:
    front: float
    back: float
    left: float
    right: float

    def __str__(self):
        return f"front: {round(self.front, FLOATING_PRECISION)}, back: {round(self.back, FLOATING_PRECISION)}, left: {round(self.left, FLOATING_PRECISION)}, right: {round(self.right, FLOATING_PRECISION)}"

    def __add__(self, other):
        return Distance(
            self.front + other.front, self.back + other.back, self.left + other.left, self.right + other.right
        )

    def __mul__(self, other):
        return Distance(self.front * other, self.back * other, self.left * other, self.right * other)
