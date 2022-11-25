import time
from threading import Thread

from src.classes.events.log import Log, generate_log
from src.clients.drone_clients.simulation_drone_client import SimulationDroneClient
from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.classes.position import Position
from src.classes.distance import Distance
from src.classes.events.metric import generate_metric


class SimulationSwarmClient(AbstractSwarmClient):
    daemon: Thread | None
    _drone_clients: list[SimulationDroneClient]
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

    def toggle_drone_synchronisation(self):
        pass

    def connect(self, uris):
        self._drone_clients.clear()
        for uri in uris:
            client = SimulationDroneClient(self.config['argos']['hostname'], uri)
            client.connect()
            self._drone_clients.append(client)

        self._is_active = True
        self.daemon = Thread(target=self._pull_task, args=[], daemon=True, name='simulation_data_pull')
        self.daemon.start()

    def disconnect(self):
        self._is_active = False
        self.daemon.join(1)
        self.daemon = None

        for drone in self._drone_clients:
            drone.disconnect()
        self._drone_clients.clear()

    def discover(self, with_limit: bool = False):
        start = int(self.config['argos']['port_start'])
        end = int(self.config['argos']['port_end'])
        timeout = int(self.config.get("grpc")["connection_timeout"])

        discovered_uris = []
        for uri in range(start, end + 1):
            client = SimulationDroneClient(self.config['argos']['hostname'], str(uri))
            client.connect()
            if client.is_ready(timeout):
                discovered_uris.append(str(uri))
            client.disconnect()

        return discovered_uris

    @property
    def uris(self):
        return [drone.uri for drone in self._drone_clients]

    def _get_telemetrics(self):
        for drone in self._drone_clients:
            metrics = drone.get_telemetrics().telemetric
            if len(metrics) > 0:
                metric = metrics[0]
                position = metric.position
                self._callbacks["metric"](
                    generate_metric(Position(position.x, position.y, position.z), self.STATUS[metric.status],
                                    drone.uri))

    def _get_distances(self):
        for drone in self._drone_clients:
            distances = drone.get_distances().distanceObstacle
            if len(distances) > 0:
                d = distances[0]
                position = d.position
                self._callbacks["mapping"](drone.uri, Position(position.x, position.y, position.z),
                                           Distance(d.front, d.back, d.left, d.right))

    def _get_logs(self):
        for drone in self._drone_clients:
            for log in drone.get_logs().logs:
                self._callbacks["logging"](generate_log("", log.message, log.level, drone.uri))

    def _pull_task(self):
        while self._is_active:
            time.sleep(0.4)
            try:
                self._get_telemetrics()
                self._get_distances()
                self._get_logs()
            except Exception as e:
                print(e)
