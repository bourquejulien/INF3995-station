import uuid
from dataclasses import dataclass

from src.classes.events.event import Event, get_timestamp_ms


def generate_mission(is_simulation: bool, total_distance: float, drone_count: int, start_time_ms: int = None,
                     end_time_ms: int = None):
    if start_time_ms is None:
        start_time_ms = get_timestamp_ms()
    return Mission(str(uuid.uuid4()), is_simulation, total_distance, drone_count, start_time_ms, end_time_ms)


@dataclass
class Mission(Event):
    is_simulation: bool
    total_distance: float
    drone_count: int
    start_time_ms: int
    end_time_ms: int

    def __lt__(self, other):
        return self.end_time_ms < other.end_time_ms
