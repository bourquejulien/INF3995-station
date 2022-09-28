from src.clients.drone_client import DroneClient
from src.services.persistent_service import PersistentService


class CommandService:

    def __init__(self, drone_client: DroneClient, persistent_service: PersistentService):
        self.droneClient = drone_client

    def start_mission(self, request_data):
        # TODO implement changing from simulation to swarm mode
        self.droneClient.start_mission()
        response = {
            "status": "success",
        }
        return response

    def end_mission(self, request_data):
        # TODO implement changing from simulation to swarm mode
        self.droneClient.end_mission()
        response = {
            "status": "success",
        }
        return response

    def discover(self):
        return self.droneClient.discover()

    def identify(self, request_data):
        self.droneClient.identify()

        response = {
            "status": "success",
        }
        return response
