from src.clients.abstract_swarm_client import AbstractSwarmClient


class StartupService:
    def __init__(self, swarm_client: AbstractSwarmClient):
        self._swarm_client = swarm_client
        self.drones_ids = []

    def start(self):
        self.drones_ids = self._swarm_client.discover()

    def connect(self, uris):
        self._swarm_client.connect(uris)

    def disconnect(self):
        self._swarm_client.disconnect()
