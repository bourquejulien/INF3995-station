from src.classes.events.metric import Metric
from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.services.mission_service import MissionService


class TelemetricsService:
    _metrics: list[Metric]

    def __init__(self, mission_service: MissionService, swarm_client: AbstractSwarmClient):
        self._mission_service = mission_service
        swarm_client.add_callback("metric", self._add)
        self._metrics = []

    def _add(self, metric: Metric):
        current_mission = self._mission_service.current_mission
        if current_mission is not None:
            metric.mission_id = current_mission.id
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

    def flush(self):
        # TODO Add data to DB and clean
        # TODO A appeler quelque part
        self._metrics.clear()

    @property
    def latest(self):
        self._metrics.sort()
        return self._metrics[-1]
