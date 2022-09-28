from src.clients.swarm_client import SwarmClient
from src.services.persistent_service import PersistentService


class CommandService:

    def __init__(self, swarm_client: SwarmClient, persistent_service: PersistentService):
        self.swarm_client = swarm_client

    def start_mission(self, request_data):
        # TODO implement changing from simulation to swarm mode
        self.swarm_client.start_mission()
        response = {
            "status": "success",
        }
        return response

    def end_mission(self, request_data):
        # TODO implement changing from simulation to swarm mode
        self.swarm_client.end_mission()
        response = {
            "status": "success",
        }
        return response

    def identify(self, request_data):
        uris = request_data.uris

        for client in self.swarm_client.drone_clients:
            if client.uri in uris:
                client.identify()

        response = {
            "status": "success",
        }
        return response
