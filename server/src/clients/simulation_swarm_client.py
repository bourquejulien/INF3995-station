import logging
import time
from threading import Thread

from src.classes.events.log import generate_log
from src.clients.drone_clients.simulation_drone_client import SimulationDroneClient
from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.classes.position import Position
from src.classes.events.metric import generate_metric
from src.exceptions.simulation_exception import SimulationException

logger = logging.getLogger(__name__)


def distance_to_position(distance_obstacle):
    front = distance_obstacle.front / 100
    back = distance_obstacle.back / 100
    left = distance_obstacle.left / 100
    right = distance_obstacle.right / 100
    positionDroneX = distance_obstacle.position.x
    positionDroneY = distance_obstacle.position.y

    positionObstacle = []
    trigger = 5.0

    if 0 < front < trigger:
        positionObstacle.append(Position(positionDroneX, positionDroneY - front, 0))
    if 0 < back < trigger:
        positionObstacle.append(Position(positionDroneX, positionDroneY + back, 0))
    if 0 < left < trigger:
        positionObstacle.append(Position(positionDroneX + left, positionDroneY, 0))
    if 0 < right < trigger:
        positionObstacle.append(Position(positionDroneX - right, positionDroneY, 0))

    return positionObstacle


class SimulationSwarmClient(AbstractSwarmClient):
    daemon: Thread | None
    _drone_clients: dict[str, SimulationDroneClient]
    _is_active: bool

    def __init__(self, config):
        super().__init__()
        self._drone_clients = {}
        self.config = config
        self.daemon = None
        self._is_active = False

    def start_mission(self):
        for drone in self._drone_clients.values():
            drone.start_mission()

    def end_mission(self):
        for drone in self._drone_clients.values():
            drone.end_mission()

    def force_end_mission(self):
        for drone in self._drone_clients.values():
            drone.force_end_mission()

    def return_to_base(self):
        threads = []
        for drone in self._drone_clients.values():
            thread = Thread(target=drone.return_to_base)
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()

    def identify(self, uris):
        for drone in self._drone_clients.values():
            if drone.uri in uris:
                drone.identify()

    def toggle_drone_synchronisation(self):
        pass

    def connect(self, uris):
        self._drone_clients.clear()
        for uri in uris:
            client = SimulationDroneClient(self.config["argos"]["hostname"], uri)
            client.connect()
            self._drone_clients[uri] = client

        self._is_active = True
        self.daemon = Thread(target=self._pull_task, args=[], daemon=True, name="simulation_data_pull")
        self.daemon.start()

    def disconnect(self):
        if self.daemon is None:
            return

        self._is_active = False
        self.daemon.join(1)
        self.daemon = None

        for drone in self._drone_clients.values():
            drone.disconnect()
        self._drone_clients.clear()

    def set_initial_positions(self, initial_data: list[(str, Position, float)]):
        pass

    def discover(self, with_limit: bool = False):
        start = int(self.config["argos"]["port_start"])
        end = int(self.config["argos"]["port_end"])
        timeout = int(self.config.get("grpc")["connection_timeout"])

        discovered_uris = []
        for uri in range(start, end + 1):
            client = SimulationDroneClient(self.config["argos"]["hostname"], str(uri))
            client.connect()
            if client.is_ready(timeout):
                discovered_uris.append(str(uri))
            client.disconnect()

        return discovered_uris

    @property
    def uris(self):
        return list(self._drone_clients.keys())

    def _get_telemetrics(self, drone: SimulationDroneClient):
        metrics = drone.get_telemetrics().telemetric
        if len(metrics) > 0:
            metric = metrics[0]
            position = metric.position
            self._callbacks["metric"](
                generate_metric(Position(position.x, position.y, position.z), self.status[metric.status], drone.uri)
            )

    def _get_distances(self, drone: SimulationDroneClient):
        distanceObstacle = drone.get_distances().distanceObstacle
        if len(distanceObstacle) > 0:
            distances = distance_to_position(distanceObstacle[0])
            position = distanceObstacle[0].position
            self._callbacks["mapping"](drone.uri, Position(position.x, position.y, position.z), distances)

    def _get_logs(self, drone: SimulationDroneClient):
        for log in drone.get_logs().logs:
            self._callbacks["logging"](generate_log("", log.message, log.level, drone.uri))

    def _pull_task(self):
        while self._is_active:
            time.sleep(0.4)
            try:
                for drone in self._drone_clients.values():
                    self._get_telemetrics(drone)
                    self._get_distances(drone)
                    self._get_logs(drone)

            except SimulationException as e:
                if e.unavailable:
                    if drone := self._drone_clients.get(e.uri):
                        drone.disconnect()
                        self._drone_clients.pop(e.uri)
                        logger.info("Drone (%s) disconnected", drone.uri)
            except Exception as e:
                logger.exception("Error during simulation pulling")
