from src.classes.events.metric import Metric
from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.services.database_service import DatabaseService
from src.services.logging_service import LoggingService
from src.services.mission_service import MissionService


class TelemetricsService:
    _mission_service: MissionService
    _database_service: DatabaseService
    _logging_service: LoggingService
    _metrics: list[Metric]
    _latest: dict[str, Metric]

    def __init__(self, swarm_client: AbstractSwarmClient, mission_service: MissionService,
                 database_service: DatabaseService, logging_service: LoggingService):
        self._mission_service = mission_service
        self._database_service = database_service
        self._logging_service = logging_service
        self._metrics = []
        self._latest = {}
        swarm_client.add_callback("metric", self._add)
        mission_service.add_flush_action(self.flush)

    def _add(self, metric: Metric):
        self._logging_service.log(f"Received position: {metric.position}, uri: {metric.uri}")
        current_mission = self._mission_service.current_mission
        if current_mission is not None:
            metric.mission_id = current_mission.id
        self._latest[metric.origin] = metric
        self._metrics.append(metric)

    def get_by_id(self, id: int):
        for metric in self._metrics:
            if metric.id == id:
                return metric
        return None

    def get_since(self, timestamp_ms: int):
        self._metrics.sort()

        for i, metric in enumerate(self._metrics):
            if timestamp_ms < metric.timestamp_ms:
                return self._metrics[i:].copy()

        return None

    def get_history(self, mission_id: str):
        self._database_service.get_metrics(mission_id)

    def flush(self):
        if self._mission_service.current_mission is not None:
            self._database_service.add_many(self._metrics)
        self._metrics.clear()
        self._latest.clear()

    @property
    def latest(self):
        return self._latest
