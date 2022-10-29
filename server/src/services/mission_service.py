from dependency_injector.providers import Configuration

from src.classes.events.event import get_timestamp_ms
from src.classes.events.mission import Mission, generate_mission
from src.exceptions.custom_exception import CustomException
from src.services.database_service import DatabaseService


class MissionService:
    _config: Configuration
    _database_service: DatabaseService
    _mission: Mission | None

    def __init__(self, config: Configuration, database_service: DatabaseService):
        self._config = config
        self._database_service = database_service
        self._mission = None

    def start_mission(self):
        if self._mission is not None:
            raise CustomException("MissionAlreadyExist", "Mission already started")

        self._mission = generate_mission(self._config.get("is_simulation"), 0, get_timestamp_ms())

    def stop_mission(self):
        mission = self._mission
        self._mission = None

        mission.end_time_ms = get_timestamp_ms()
        mission.total_distance = ...  # TODO Ajouter a partir d'un callback a TelemetricService?

        # TODO Save mission to DB
        return mission

    def get_missions_range(self, start_timestamp: int, end_timestamp: int = 0):
        # TODO USE DB
        ...

    def get_mission_by_id(self, id: str):
        # TODO USE DB
        ...

    @property
    def current_mission(self) -> Mission:
        return self._mission
