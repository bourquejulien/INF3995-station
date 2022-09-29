import grpc

from src.clients.drone_clients.sim_drone_client import SimDroneClient

from src.clients.swarm_client import SwarmClient
from src.config import config


class SimSwarmClient(SwarmClient):
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
            client = SimDroneClient(uri)
            client.connect()
            self._drone_clients.append(client)

    def disconnect(self):
        for drone in self.drone_clients:
            drone.disconnect()

    def discover(self):
        port = config["argos_url"]["port"]
        return [port, port + 1]
