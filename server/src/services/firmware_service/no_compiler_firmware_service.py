from cflib.bootloader import Bootloader, TargetTypes, FlashArtifact, Target

from src.services.command_service import CommandService
from src.services.firmware_service.abstract_firmware_service import AbstractFirmwareService


class NoCompilerFirmwareService(AbstractFirmwareService):
    command_service: CommandService

    def __init__(self, command_service: CommandService):
        self.command_service = command_service

    def flash_data(self, data: bytes):
        self.command_service.disconnect()
        self._flash(data)
        uris = self.command_service.discover()
        self.command_service.connect(uris)

    def flash_repo(self):
        pass

    def edit(self, path: str, data: bytes):
        pass

    def get_file(self, path: str):
        return b""

    def close(self, exit_info: tuple):
        pass

    def _flash(self, data: bytes):
        uris = self.command_service.discover()
        bootloaders = [Bootloader(uri) for uri in uris]

        for bootloader in bootloaders:
            bootloader.start_bootloader(warm_boot=True)
            target = Target("", "stm32", TargetTypes.STM32)
            bootloader._internal_flash(FlashArtifact(data, target))

        for bootloader in bootloaders:
            bootloader.reset_to_firmware()
