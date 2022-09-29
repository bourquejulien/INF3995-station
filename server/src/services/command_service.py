from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.services.startup_service import StartupService


class CommandService:

    def __init__(self, swarm_client: AbstractSwarmClient, persistent_service: StartupService):
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

    def identify(self, uris):
        for client in self.swarm_client.drone_clients:
            if client.uri in uris:
                client.identify()

        response = {
            "status": "success",
        }
        return response
