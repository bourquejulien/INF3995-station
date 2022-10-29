from dataclasses import dataclass

from src.classes.distance import Distance
from src.classes.position import Position


@dataclass
class MappingPoint:
    position: Position
    distance: Distance
