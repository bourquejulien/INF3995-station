from dataclasses import dataclass

from src.classes.events.event import Event, get_timestamp_ms
from src.classes.position import Position


def generate_metric(position: Position, status: str, origin: str):
    return Metric(None, get_timestamp_ms(), position, status, origin)


@dataclass
class Metric(Event):
    timestamp_ms: int
    position: Position
    status: str
    origin: str
