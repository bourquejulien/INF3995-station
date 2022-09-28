from abc import ABC, abstractmethod


class SwarmClient(ABC):
    _drone_clients: list

    @property
    def drone_clients(self):
        return self._drone_clients

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
