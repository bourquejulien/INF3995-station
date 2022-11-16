from dependency_injector.providers import Configuration

from src.services.command_service import CommandService
from src.services.firmware_service.no_compiler_firmware_service import NoCompilerFirmwareService
from src.services.firmware_service.remote_compiler_client import RemoteCompilerClient


class FirmwareService(NoCompilerFirmwareService):
    remote_compiler_client: RemoteCompilerClient

    def __init__(self, config: Configuration, command_service: CommandService):
        super().__init__(command_service)
        self.remote_compiler_client = RemoteCompilerClient(config["remote_compiler"]["connection_string"]).__enter__()

    def flash_data(self, data: bytes):
        super().flash_data(data)

    def flash_repo(self):
        blocks = self.remote_compiler_client.build()
        data = b"".join(blocks)
        self.flash_data(data)

    def edit(self, path: str, data: bytes):
        self.remote_compiler_client.edit(path, data)

    def get_file(self, path: str):
        file = self.remote_compiler_client.get(path)
        return file.encode("utf-8")

    def close(self, exit_info: tuple):
        self.remote_compiler_client.__exit__(*exit_info)
