from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional


def get_timestamp_ms():
    return int(datetime.now(timezone.utc).timestamp() * 1000)


@dataclass
class Event:
    id: Optional[str]

    def to_json(self):
        data = asdict(self)
        if self.id is not None:
            data["_id"] = self.id
        data.pop("id")
        return data

    def __str__(self):
        return self.to_json().__str__()
