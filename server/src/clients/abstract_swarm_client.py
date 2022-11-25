from abc import ABC, abstractmethod


class AbstractSwarmClient(ABC):
    STATUS = ["Idle", "Identify", "Takeoff", "Exploration", "Landing", "EmergencyStop", "ChooseAngle"]

    def __init__(self):
        self._callbacks = {}

    @abstractmethod
    def start_mission(self):
        pass

    @abstractmethod
    def end_mission(self):
        pass

    @abstractmethod
    def force_end_mission(self):
        pass

    @abstractmethod
    def identify(self, uris):
        pass

    @abstractmethod
    def toggle_drone_synchronisation(self):
        pass

    @abstractmethod
    def connect(self, uris):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def discover(self, with_limit: bool):
        pass

    @property
    @abstractmethod
    def uris(self):
        pass

    def add_callback(self, name: str, func):
        self._callbacks[name] = func
