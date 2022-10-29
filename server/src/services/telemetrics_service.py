from dependency_injector.wiring import inject, Provide, Container

from src.classes.events.metric import Metric
from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.services.mission_service import MissionService


class TelemetricsService:
    _metrics: list[Metric]

    def __init__(self, swarm_client: AbstractSwarmClient):
        swarm_client.add_callback("metric", self._add)
        self._metrics = []

    @inject
    def _add(self, metric: Metric, mission_service: MissionService = Provide[Container.mission_service]):
        current_mission = mission_service.current_mission
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
        # TODO Il faut ajouter les Metric au DatabaseService
        self._metrics.clear()

    @property
    def latest(self):
        self._metrics.sort()
        return self._metrics[-1]
