from src.clients.drone_clients.simulation_drone_client import SimulationDroneClient

from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.config import config


class SimulationSwarmClient(AbstractSwarmClient):
    def __init__(self):
        self._drone_clients = []

    def start_mission(self):
        for drone in self._drone_clients:
            drone.start_mission()

    def end_mission(self):
        for drone in self._drone_clients:
            drone.end_mission()

    def force_end_mission(self):
        # TODO
        pass

    def identify(self, uris):
        for drone in self._drone_clients:
            if drone.uri in uris:
                drone.identify()

    def connect(self, uris):
        for uri in uris:
            client = SimulationDroneClient(uri)
            client.connect()
            self._drone_clients.append(client)

    def disconnect(self):
        for drone in self._drone_clients:
            drone.disconnect()

    def discover(self):
        port = config["argos_url"]["port"]
        return [str(port), str(port + 1)]
