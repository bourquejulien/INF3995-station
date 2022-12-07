from dataclasses import dataclass

FLOATING_PRECISION = 2


@dataclass
class Vec2:
    x: float
    y: float

    def __str__(self):
        return f"x: {round(self.x, FLOATING_PRECISION)}, y: {round(self.y, FLOATING_PRECISION)}"
