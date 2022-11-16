from src.services.firmware_service.abstract_firmware_service import AbstractFirmwareService


class FirmwareService(AbstractFirmwareService):

    def flash_data(self, data: bytes):
        pass

    def flash_repo(self):
        pass

    def edit(self, path: str, data: bytes):
        pass

    def get_file(self, path: str):
        return b""
