from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.exceptions.custom_exception import CustomException
from src.services.mission_service import MissionService


class CommandService:
    swarm_client: AbstractSwarmClient
    mission_service: MissionService

    def __init__(self, swarm_client: AbstractSwarmClient, mission_service: MissionService):
        self.swarm_client = swarm_client
        self.mission_service = mission_service

    def start_mission(self):
        try:
            self.mission_service.start_mission()
            self.swarm_client.start_mission()
            return self.mission_service.current_mission.id
        except CustomException as e:
            raise e

    def end_mission(self):
        try:
            self.swarm_client.end_mission()
            self.mission_service.stop_mission()
        except CustomException as e:
            raise e

    def force_end_mission(self, request_data):
        try:
            self.swarm_client.force_end_mission()
            self.mission_service.stop_mission()
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
