from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.exceptions.custom_exception import CustomException
from src.services.logging_service import LoggingService
from src.services.mission_service import MissionService


def _format_command(command, info: str = None):
    data = f"cmd: {command.__name__}"
    return data + f", {info}" if info is not None else data


class CommandService:
    _swarm_client: AbstractSwarmClient
    _mission_service: MissionService
    _logging_service: LoggingService

    def __init__(self, swarm_client: AbstractSwarmClient, mission_service: MissionService,
                 logging_service: LoggingService):
        self._swarm_client = swarm_client
        self._mission_service = mission_service
        self._logging_service = logging_service

    def start_mission(self):
        try:
            mission = self._mission_service.start_mission()
            self._swarm_client.start_mission()
            self._logging_service.log(_format_command(self.start_mission, f"id: {mission.id}"))
        except CustomException as e:
            raise e
        return mission

    def end_mission(self):
        try:
            mission = self._mission_service.current_mission

            if mission is not None:
                self._logging_service.log(_format_command(self.end_mission, f"id: {mission.id}"))
            else:
                self._logging_service.log(_format_command(self.end_mission, "no mission running"))

            self._swarm_client.end_mission()
            self._mission_service.end_mission()

        except CustomException as e:
            raise e

    def force_end_mission(self):
        try:
            self._swarm_client.force_end_mission()
            mission = self._mission_service.end_mission()
            if mission is not None:
                self._logging_service.log(_format_command(self.force_end_mission, f"id: {mission.id}"))
            else:
                self._logging_service.log(_format_command(self.force_end_mission, "no mission running"))
        except CustomException as e:
            raise e

    def identify(self, uris):
        try:
            self._swarm_client.identify(uris)
            self._logging_service.log(_format_command(self.identify, f"Uris: {uris}"))
        except CustomException as e:
            raise e

    def connect(self, uris):
        try:
            self._swarm_client.connect(uris)
            self._logging_service.log(_format_command(self.connect, f"Uris: {uris}"))
        except CustomException as e:
            raise e

    def disconnect(self):
        try:
            self._swarm_client.disconnect()
            self._logging_service.log(_format_command(self.disconnect))
        except CustomException as e:
            raise e

    def discover(self) -> list:
        try:
            self._logging_service.log(_format_command(self.discover))
            return self._swarm_client.discover()
        except CustomException as e:
            raise e
