from src.clients.swarm_client import SwarmClient


class PersistentService:
    def __init__(self, swarm_client: SwarmClient):
        self._swarmCLient = swarm_client
        self.drones_ids = []

    def start(self):
        self.drones_ids = self._swarmCLient.discover()

    def connect(self, uris):
        self._swarmCLient.connect(uris)

    def disconnect(self):
        self._swarmCLient.disconnect()
