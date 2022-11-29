import os
import sys
import time
from contextlib import contextmanager

from cflib.bootloader import Bootloader, TargetTypes, FlashArtifact, Target

from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.services.command_service import CommandService
from src.services.firmware_service.abstract_firmware_service import AbstractFirmwareService

BOOT_TIME = 2


@contextmanager
def silence():
    with open(os.devnull, "w") as null:
        save = sys.stdout
        sys.stdout = null
        try:
            yield
        finally:
            sys.stdout = save


class NoCompilerFirmwareService(AbstractFirmwareService):
    command_service: CommandService
    swarm_client: AbstractSwarmClient

    def __init__(self, command_service: CommandService, swarm_client: AbstractSwarmClient):
        self.command_service = command_service
        self.swarm_client = swarm_client

    def flash_data(self, data: bytes):
        with self.command_service.disable():
            uris = self.swarm_client.uris
            uris_no_param = [uri[0:uri.find("?")] for uri in self.swarm_client.uris]

            self.swarm_client.disconnect()
            self._flash(data, uris_no_param)
            time.sleep(BOOT_TIME)
            self.swarm_client.connect(uris)

    def flash_repo(self):
        pass

    def edit(self, path: str, data: bytes):
        pass

    def get_file(self, path: str):
        return b""

    def close(self, exit_info: tuple):
        pass

    def _flash(self, data: bytes, uris: list[str]):
        bootloaders = [Bootloader(uri) for uri in uris]

        for bootloader in bootloaders:
            bootloader.start_bootloader(warm_boot=True)
            target = Target("", "stm32", TargetTypes.STM32)

            with silence():
                bootloader._internal_flash(FlashArtifact(data, target))

            bootloader.reset_to_firmware()
