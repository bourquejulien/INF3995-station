from src.classes.events.metric import Metric
from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.services.mission_service import MissionService


class TelemetricsService:
    _mission_service: MissionService
    _metrics: list[Metric]

    def __init__(self, swarm_client: AbstractSwarmClient, mission_service: MissionService):
        self._mission_service = mission_service
        self._metrics = []
        swarm_client.add_callback("metric", self._add)

    def _add(self, metric: Metric):
        print(metric)
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

    # TODO Ajouter un call pour aller rechercher dans l'historique de la DB

    def flush(self):
        # TODO Add data to DB and clean
        # TODO Il faut ajouter les Metric au DatabaseService
        self._metrics.clear()

    @property
    def latest(self):
        self._metrics.sort()
        return self._metrics[-1]
