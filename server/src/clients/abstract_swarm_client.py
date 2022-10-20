from abc import ABC, abstractmethod


class AbstractSwarmClient(ABC):
    @abstractmethod
    def start_mission(self):
        pass

    @abstractmethod
    def end_mission(self):
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
