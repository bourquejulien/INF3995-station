from src.clients.drone_client import DroneClient


class SimulationClient(DroneClient):
    def identify(self):
        pass

    def start_mission(self):
        pass

    def end_mission(self):
        pass

    def connect(self, uri):
        pass

    def disconnect(self):
        pass

    def discover(self):
        pass