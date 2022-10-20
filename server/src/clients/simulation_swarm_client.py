from src.clients.drone_clients.simulation_drone_client import SimulationDroneClient
from src.clients.abstract_swarm_client import AbstractSwarmClient


class SimulationSwarmClient(AbstractSwarmClient):
    def __init__(self, config):
        self._drone_clients = []
        self.config = config
        self.connect(self.discover())

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
            client = SimulationDroneClient(self.config['argos']['hostname'], uri)
            client.connect()
            self._drone_clients.append(client)

    def disconnect(self):
        for drone in self._drone_clients:
            drone.disconnect()

    def discover(self):
        return [str(self.config['argos']['port']), str(self.config['argos']['port'] + 1)]
