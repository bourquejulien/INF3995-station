import json
import time
from threading import Thread

from src.clients.drone_clients.simulation_drone_client import SimulationDroneClient
from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.classes.position import Position
from src.classes.distance import Distance
from src.classes.events.metric import generate_metric


class SimulationSwarmClient(AbstractSwarmClient):
    daemon: Thread | None
    _is_active: bool

    def __init__(self, config):
        super().__init__()
        self._drone_clients = []
        self.config = config
        self.daemon = None
        self._is_active = False

    def start_mission(self):
        for drone in self._drone_clients:
            drone.start_mission()

    def end_mission(self):
        for drone in self._drone_clients:
            drone.end_mission()

    def force_end_mission(self):
        for drone in self._drone_clients:
            drone.force_end_mission()

    def identify(self, uris):
        for drone in self._drone_clients:
            if drone.uri in uris:
                drone.identify()

    def connect(self, uris):
        for uri in uris:
            client = SimulationDroneClient(self.config['argos']['hostname'], uri)
            client.connect()
            self._drone_clients.append(client)

        self._is_active = True
        self.daemon = Thread(target=self._pull_task, args=[], daemon=True, name='simulation_data_pull')
        self.daemon.start()

    def disconnect(self):
        self.daemon.join(500)
        self.daemon = None

        for drone in self._drone_clients:
            drone.disconnect()

    def discover(self):
        return [str(self.config['argos']['port']), str(self.config['argos']['port'] + 1)]

    def _get_telemetrics(self):
        for drone in self._drone_clients:
            metrics = drone.get_telemetrics()
            for m in metrics.telemetric:
                self._callbacks["metric"](generate_metric(Position(m.posX, m.posY, m.posZ), m.status, drone.uri))

    def _get_distances(self):
        for drone in self._drone_clients:
            dist = drone.get_distances()
            for d in dist.distanceObstacle:
                self._callbacks["mapping"](drone.uri, Position(d.posX, d.posY, d.posZ),
                                           Distance(d.front, d.back, d.left, d.right))

    def _pull_task(self):
        while self._is_active:
            time.sleep(0.4)
            self._get_telemetrics()
            self._get_distances()
