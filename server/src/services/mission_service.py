from contextlib import contextmanager
from threading import Lock

from dependency_injector.providers import Configuration

from src.classes.events.event import get_timestamp_ms
from src.classes.events.mission import Mission, generate_mission
from src.exceptions.custom_exception import CustomException
from src.services.database_service import DatabaseService


class MissionService:
    _mutex: Lock
    _config: Configuration
    _database_service: DatabaseService
    _mission: Mission | None
    _flush_callbacks: list

    def __init__(self, config: Configuration, database_service: DatabaseService):
        self._mutex = Lock()
        self._mission = None
        self._flush_callbacks = []
        self._config = config
        self._database_service = database_service

    def start_mission(self, drone_count: int):
        with self._mutex:
            if self._mission is not None:
                raise CustomException("MissionAlreadyExist", "Mission already started")

            self.flush()
            self._mission = generate_mission(self._config.get("is_simulation"), 0, drone_count, get_timestamp_ms())
            return self._mission

    def end_mission(self):
        with self._mutex:
            mission = self.flush()

        if mission is None:
            return None

        mission.end_time_ms = get_timestamp_ms()

        self._database_service.add(mission)

    def return_to_base(self):
        with self._mutex:
            mission = self.flush()

        if mission is None:
            return None

        mission.end_time_ms = get_timestamp_ms()

        self._database_service.add(mission)

    def flush(self):
        for flush in self._flush_callbacks:
            flush()

        mission = self._mission
        self._mission = None

        return mission

    def get_last_missions(self, mission_number: int):
        return self._database_service.get_missions(mission_number)

    def get_mission_by_id(self, id: str):
        self._database_service.get_mission(id)

    def add_flush_action(self, action):
        self._flush_callbacks.append(action)

    @property
    def current_mission(self) -> Mission:
        return self._mission
