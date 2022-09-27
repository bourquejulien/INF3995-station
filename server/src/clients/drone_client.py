from abc import ABC, abstractmethod


class DroneClient(ABC):
    @abstractmethod
    def identify(self):
        pass

    @abstractmethod
    def start_mission(self):
        pass

    @abstractmethod
    def end_mission(self):
        pass

    @abstractmethod
    def connect(self, uri):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def discover(self):
        pass
