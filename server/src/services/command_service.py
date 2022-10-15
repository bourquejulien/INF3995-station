from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.services.startup_service import StartupService
from src.exceptions.custom_exception import CustomException


class CommandService:

    def __init__(self, swarm_client: AbstractSwarmClient, persistent_service: StartupService):
        self.swarm_client = swarm_client

    def start_mission(self, request_data):
        try:
            self.swarm_client.start_mission()
        except CustomException as e:
            raise e

    def end_mission(self, request_data):
        try:
            self.swarm_client.end_mission()
        except CustomException as e:
            raise e

    def identify(self, uris):
        try:
            self.swarm_client.identify(uris)
        except CustomException as e:
            raise e
