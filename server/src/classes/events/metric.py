from dataclasses import dataclass

from src.classes.events.event import Event, get_timestamp_ms
from src.classes.position import Position


def generate_metric(position: Position, status: str, uri: str, mission_id: str = "", battery_level: float = 0.0):
    return Metric(None, get_timestamp_ms(), position, status, uri, mission_id, battery_level)


@dataclass
class Metric(Event):
    timestamp_ms: int
    position: Position
    status: str
    uri: str
    mission_id: str
    battery_level: float

    def __lt__(self, other):
        return self.timestamp_ms < other.timestamp_ms
