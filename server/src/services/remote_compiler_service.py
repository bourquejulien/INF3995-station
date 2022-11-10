from cflib.bootloader import Bootloader, TargetTypes, FlashArtifact

from src.clients.abstract_swarm_client import AbstractSwarmClient


class RemoteCompilerService:
    swarm_client: AbstractSwarmClient

    def __init__(self, swarm_client: AbstractSwarmClient):
        self.swarm_client = swarm_client

    def flash_file(self):
        ...

    def flash_repo(self):
        ...

    def edit(self):
        ...

    def get_file(self):
        ...

    def _flash(self, data: bytes):
        uris = self.swarm_client.discover()
        bootloaders = [Bootloader(uri) for uri in uris]

        for bootloader in bootloaders:
            bootloader.start_bootloader(warm_boot=True)
            target = bootloader.get_target(TargetTypes.STM32)
            bootloader._internal_flash(FlashArtifact(data, target))

        for bootloader in bootloaders:
            bootloader.reset_to_firmware()
