from src.clients.drone_clients.drone_client import DroneClient


class SimDroneClient(DroneClient):
    def __init__(self, uri):
        self.uri = uri

    def identify(self):
        pass

    def start_mission(self):
        pass

    def end_mission(self):
        pass

    def connect(self):
        pass

    def disconnect(self):
        pass
