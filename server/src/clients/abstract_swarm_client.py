from abc import ABC, abstractmethod


class AbstractSwarmClient(ABC):
    # Pourquoi STATUS en majuscules?
    STATUS = ["Idle", "Identify", "Takeoff", "Exploration", "Landing", "EmergencyStop", "ChooseAngle", "Crashed"]

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
    def connect(self, uris):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def discover(self):
        pass

    @abstractmethod
    def is_crashed(self):
        pass

    def add_callback(self, name: str, func):
        self._callbacks[name] = func
