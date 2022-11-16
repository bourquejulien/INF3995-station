from cflib.bootloader import Bootloader, TargetTypes, FlashArtifact, Target

from src.services.command_service import CommandService
from src.services.firmware_service.abstract_firmware_service import AbstractFirmwareService
from src.services.firmware_service.no_compiler_firmware_service import NoCompilerFirmwareService


class FirmwareService(AbstractFirmwareService):
    command_service: CommandService
    no_compiler_firmware_service: NoCompilerFirmwareService

    def __init__(self, command_service: CommandService):
        self.command_service = command_service
        self.no_compiler_firmware_service = NoCompilerFirmwareService(command_service)

    def flash_data(self, data: bytes):
        self.no_compiler_firmware_service.flash_data(data)

    def flash_repo(self):
        # TODO
        ...

    def edit(self, path: str, data: bytes):
        # TODO
        ...

    def get_file(self, path: str):
        # TODO
        return b""

    def _flash(self, data: bytes):
        self.no_compiler_firmware_service._flash(data)
