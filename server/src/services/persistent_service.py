from src.clients.drone_client import DroneClient


class PersistentService:
    def __init__(self, drone_client: DroneClient):
        self._droneClient = drone_client
        self.drones_ids = []

    def start(self):
        self.drones_ids = self._droneClient.discover()

    def connect(self, uri):
        self._droneClient.connect(uri)

    def disconnect(self):
        self._droneClient.disconnect()

