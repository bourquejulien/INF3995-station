from contextlib import contextmanager
from threading import Lock

from src.classes.position import Position
from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.exceptions.custom_exception import CustomException
from src.services.logging_service import LoggingService
from src.services.mission_service import MissionService


def _format_command(command, info: str = None):
    data = f"cmd: {command.__name__}"
    return data + f", {info}" if info is not None else data


class CommandService:
    _mutex: Lock
    _is_enabled: bool
    _swarm_client: AbstractSwarmClient
    _mission_service: MissionService
    _logging_service: LoggingService

    def __init__(self, swarm_client: AbstractSwarmClient, mission_service: MissionService,
                 logging_service: LoggingService):
        self._mutex = Lock()
        self._is_enabled = True
        self._swarm_client = swarm_client
        self._mission_service = mission_service
        self._logging_service = logging_service

    @contextmanager
    def disable(self):
        with self._mutex:
            if self._mission_service.current_mission is not None:
                raise CustomException("MissionEnabled", "Cannot disable missions while a mission is active")
            self._is_enabled = False
        try:
            yield
        finally:
            self._is_enabled = True

    def start_mission(self):
        try:
            with self._mutex:
                self._disabled_guard()

                mission = self._mission_service.start_mission(len(self._swarm_client.uris))
                self._swarm_client.start_mission()
                self._logging_service.log(_format_command(self.start_mission, f"id: {mission.id}"))
        except CustomException as e:
            raise e
        return mission

    def end_mission(self):
        try:
            with self._mutex:
                self._disabled_guard()

                mission = self._mission_service.current_mission

                if mission is not None:
                    self._logging_service.log(_format_command(self.end_mission, f"id: {mission.id}"))
                else:
                    self._logging_service.log(_format_command(self.end_mission, "No mission running"))

                self._swarm_client.end_mission()
                self._mission_service.end_mission()

        except CustomException as e:
            raise e

    def force_end_mission(self):
        try:
            with self._mutex:
                self._disabled_guard()
                self._swarm_client.force_end_mission()
                mission = self._mission_service.end_mission()
                if mission is not None:
                    self._logging_service.log(_format_command(self.force_end_mission, f"id: {mission.id}"))
                else:
                    self._logging_service.log(_format_command(self.force_end_mission, "No mission running"))
        except CustomException as e:
            raise e

    def return_to_base(self):
        try:
            with self._mutex:
                self._disabled_guard()
                self._swarm_client.return_to_base()
                mission = self._mission_service.end_mission()
                if mission is not None:
                    self._logging_service.log(_format_command(self.return_to_base, f"id: {mission.id}"))
                else:
                    self._logging_service.log(_format_command(self.return_to_base, "no mission running"))
        except CustomException as e:
            raise e

    def identify(self, uris):
        try:
            self._disabled_guard()
            self._swarm_client.identify(uris)
            self._logging_service.log(_format_command(self.identify, f"Uris: {uris}"))
        except CustomException as e:
            raise e

    def toggle_synchronization(self):
        try:
            self._swarm_client.toggle_drone_synchronisation()
            self._logging_service.log(_format_command(self.toggle_synchronization))
        except CustomException as e:
            raise e

    def set_initial_positions(self, initial_data: list[(str, Position, float)]) -> list:
        try:
            self._disabled_guard()
            self._logging_service.log(_format_command(self.set_initial_positions))
            return self._swarm_client.set_initial_positions(initial_data)
        except CustomException as e:
            raise e

    def connect(self, uris):
        try:
            self._disabled_guard()
            self._swarm_client.connect(uris)
            self._logging_service.log(_format_command(self.connect, f"Uris: {uris}"))
        except CustomException as e:
            raise e

    def disconnect(self):
        try:
            self._disabled_guard()
            self._swarm_client.disconnect()
            self._logging_service.log(_format_command(self.disconnect))
        except CustomException as e:
            raise e

    def discover(self) -> list:
        try:
            self._disabled_guard()
            self._logging_service.log(_format_command(self.discover))
            return self._swarm_client.discover()
        except CustomException as e:
            raise e

    @property
    def is_enabled(self) -> bool:
        return self._is_enabled

    def _disabled_guard(self):
        if not self._is_enabled:
            raise CustomException("CommandDisabled", "Commands are disabled")
