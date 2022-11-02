from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.exceptions.custom_exception import CustomException
from dependency_injector.providers import Configuration
from src.classes.events.mission import generate_mission


class CommandService:
    _config: Configuration

    def __init__(self, swarm_client: AbstractSwarmClient, config: Configuration):
        self.swarm_client = swarm_client
        self._config = config

    def start_mission(self):
        try:
            self.swarm_client.start_mission()
        except CustomException as e:
            raise e
        return generate_mission(self._config['is_simulation'])

    def end_mission(self):
        try:
            self.swarm_client.end_mission()
        except CustomException as e:
            raise e

    def force_end_mission(self, request_data):
        try:
            self.swarm_client.force_end_mission()
        except CustomException as e:
            raise e

    def identify(self, uris):
        try:
            self.swarm_client.identify(uris)
        except CustomException as e:
            raise e

    def connect(self, uris):
        try:
            self.swarm_client.connect(uris)
        except CustomException as e:
            raise e

    def disconnect(self):
        try:
            self.swarm_client.disconnect()
        except CustomException as e:
            raise e

    def discover(self) -> list:
        try:
            return self.swarm_client.discover()
        except CustomException as e:
            raise e

    def get_position(self):
        try:
            return self.swarm_client.get_position()
        except CustomException as e:
            raise e

    
