from abc import ABC, abstractmethod


class DroneClient(ABC):
    uri: str

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
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

