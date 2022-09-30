from src.clients.drone_clients.simulation_drone_client import SimulationDroneClient

from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.config import config


class SimulationSwarmClient(AbstractSwarmClient):
    def __init__(self):
        self.drone_clients = []

    @property
    def drone_clients(self):
        return self._drone_clients

    def start_mission(self):
        for drone in self.drone_clients:
            drone.start_mission()

    def end_mission(self):
        for drone in self.drone_clients:
            drone.end_mission()

    def connect(self, uris):
        for uri in uris:
            client = SimulationDroneClient(uri)
            client.connect()
            self._drone_clients.append(client)

    def disconnect(self):
        for drone in self.drone_clients:
            drone.disconnect()

    def discover(self):
        port = config["argos_url"]["port"]
        return [str(port), str(port + 1)]

    @drone_clients.setter
    def drone_clients(self, value):
        self._drone_clients = value
