from abc import ABC, abstractmethod


class AbstractFirmwareService(ABC):
    @abstractmethod
    def flash_data(self, data: bytes):
        pass

    @abstractmethod
    def flash_repo(self):
        pass

    @abstractmethod
    def edit(self, path: str, data: bytes):
        pass

    @abstractmethod
    def get_file(self, path: str):
        pass

    @abstractmethod
    def close(self, exit_info: tuple):
        pass
