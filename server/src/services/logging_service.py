from src.classes.events.log import Log
from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.services.mission_service import MissionService
from src.services.database_service import DatabaseService


class LoggingService:
    _logs: list[Log]
    _mission_service: MissionService
    _database_service: DatabaseService

    def __init__(self, swarm_client: AbstractSwarmClient, mission_service: MissionService, database_service: DatabaseService):
        self._logs = []
        self._mission_service = mission_service
        self._database_service = database_service
        swarm_client.add_callback("logging", self._add)
        mission_service.add_flush_action(self.flush)

    def _add(self, log: Log):
        current_mission = self._mission_service.current_mission
        if current_mission is not None:
            log.mission_id = current_mission.id
        self._logs.append(log)

    def get_since(self, timestamp_ms: int):
        self._logs.sort()

        for i, log in enumerate(self._logs):
            if timestamp_ms < log.timestamp_ms:
                return self._logs[i:].copy()

        return None

    # TODO Ajouter un call pour aller rechercher dans l'historique de la DB
    def get_logs(self, mission_id: str):
        return self._database_service.get_logs(mission_id)

    def flush(self):
        # TODO Add data to DB and clean
        self._logs.clear()
