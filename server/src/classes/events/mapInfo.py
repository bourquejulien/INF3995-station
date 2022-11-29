from dataclasses import dataclass

from src.classes.events.event import Event, get_timestamp_ms
from src.classes.position import Position

FLOATING_PRECISION = 2

def generate_mapInfo(uri: str, position: Position, distance: Position):
    return MapInfo(None, get_timestamp_ms(), uri, position, distance)

@dataclass
class MapInfo(Event):
    timestamp_ms: int
    uri: str
    position: Position
    distance: list[Position]

    def __str__(self):
        return f"x: {round(self.position.x, FLOATING_PRECISION)}, y: {round(self.position.y, FLOATING_PRECISION)}, z: {round(self.position.z, FLOATING_PRECISION)}"