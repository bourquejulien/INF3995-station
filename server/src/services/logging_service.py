from dependency_injector.wiring import inject, Provide, Container

from src.classes.events.log import Log
from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.services.mission_service import MissionService


class LoggingService:
    _logs: list[Log]

    def __init__(self, swarm_client: AbstractSwarmClient):
        self._logs = []
        swarm_client.add_callback("logging", self._add)

    @inject
    def _add(self, log: Log, mission_service: MissionService = Provide[Container.mission_service]):
        current_mission = mission_service.current_mission
        if current_mission is not None:
            log.mission_id = current_mission.id
        self._logs.append(log)

    def get_since(self, timestamp_ms: int):
        self._logs.sort()

        for i, log in enumerate(self._logs):
            if timestamp_ms < log.timestamp_ms:
                return self._logs[i:].copy()

        return None

    def flush(self):
        # TODO Add data to DB and clean
        self._logs.clear()
