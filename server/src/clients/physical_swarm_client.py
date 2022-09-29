import logging

import cflib
from cflib import crtp

from src.clients.drone_clients.physical_drone_client import PhysicalDroneClient
from src.clients.abstract_swarm_client import AbstractSwarmClient

logging.basicConfig(level=logging.ERROR)


class PhysicalSwarmClient(AbstractSwarmClient):
    base_uri = 0xE7E7E7E750

    def __init__(self):
        crtp.init_drivers(enable_debug_driver=False)
        self._drone_clients = []

    @property
    def drone_clients(self):
        return self._drone_clients

    def connect(self, uris):
        for uri in uris:
            client = PhysicalDroneClient(uri)
            client.connect()
            self._drone_clients.append(client)

    def disconnect(self):
        for drone in self.drone_clients:
            drone.disconnect()

    def start_mission(self):
        for drone in self.drone_clients:
            drone.start_mission()

    def end_mission(self):
        for drone in self.drone_clients:
            drone.end_mission()

    def discover(self):
        available_devices = []
        for i in range(5):
            devices_on_address = cflib.crtp.scan_interfaces(self.base_uri + i)
            available_devices.extend(device[0] for device in devices_on_address)
        return available_devices
