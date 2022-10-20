from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.exceptions.custom_exception import CustomException


class CommandService:
    def __init__(self, swarm_client: AbstractSwarmClient):
        self.swarm_client = swarm_client

    def start_mission(self):
        try:
            self.swarm_client.start_mission()
        except CustomException as e:
            raise e

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

    def discover(self):
        try:
            self.swarm_client.discover()
        except CustomException as e:
            raise e
