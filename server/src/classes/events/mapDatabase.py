from dataclasses import dataclass

from src.classes.events.event import Event, get_timestamp_ms
from src.classes.vec2 import Vec2


def generate_mapDatabase(positionObstacle: list[Vec2], mission_id: str = ""):
    return MapDatabase(None, positionObstacle, mission_id)


@dataclass
class MapDatabase(Event):
    obstaclePosition: list[Vec2]
    mission_id: str
