from dataclasses import dataclass

from src.classes.events.event import Event, get_timestamp_ms


def generate_log(mission_id: str, message: str, level: str, origin: str):
    return Log(None, get_timestamp_ms(), mission_id, message, level, origin)


@dataclass
class Log(Event):
    timestamp_ms: int
    mission_id: str
    message: str
    level: str
    origin: str

    def __lt__(self, other):
        return self.timestamp_ms < other.timestamp_ms
