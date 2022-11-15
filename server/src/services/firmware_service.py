from cflib.bootloader import Bootloader, TargetTypes, FlashArtifact, Target

from src.services.command_service import CommandService


class FirmwareService:
    command_service: CommandService

    def __init__(self, command_service: CommandService):
        self.command_service = command_service

    def flash_data(self, data: bytes):
        self.command_service.disconnect()
        self._flash(data)
        uris = self.command_service.discover()
        self.command_service.connect(uris)

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
        uris = self.command_service.discover()
        bootloaders = [Bootloader(uri) for uri in uris]

        for bootloader in bootloaders:
            bootloader.start_bootloader(warm_boot=True)
            target = Target("", "stm32", TargetTypes.STM32)
            bootloader._internal_flash(FlashArtifact(data, target))

        for bootloader in bootloaders:
            bootloader.reset_to_firmware()
