import uuid
from dataclasses import dataclass

from src.classes.events.event import Event, get_timestamp_ms


def generate_mission(is_simulation: bool, start_time_ms: int = None, end_time_ms: int = None):
    if start_time_ms is None:
        start_time_ms = get_timestamp_ms()
    return Mission(str(uuid.uuid4()), is_simulation, start_time_ms, end_time_ms)


@dataclass
class Mission(Event):
    is_simulation: bool
    start_time_ms: int
    end_time_ms: int
