import logging

import cflib
from cflib import crtp
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.swarm import CachedCfFactory, Swarm

from src.clients.drone_clients.physical_drone_client import *
from src.clients.abstract_swarm_client import AbstractSwarmClient

logging.basicConfig(level=logging.ERROR)


class PhysicalSwarmClient(AbstractSwarmClient):
    base_uri = 0xE7E7E7E750
    _swarm: Swarm

    def __init__(self):
        self._factory = CachedCfFactory(rw_cache='./cache')
        crtp.init_drivers(enable_debug_driver=False)

    def connect(self, uris):
        self._swarm = Swarm(uris, factory=self._factory)
        self._swarm.open_links()
        self._swarm.parallel_safe(self._enable_callbacks)
        self._swarm.parallel_safe(self._set_params)

    def _enable_callbacks(self, scf: SyncCrazyflie):
        scf.cf.connected.add_callback(self._connected)
        scf.cf.disconnected.add_callback(self._disconnected)
        scf.cf.connection_failed.add_callback(self._connection_failed)
        scf.cf.connection_lost.add_callback(self._connection_lost)
        scf.cf.console.receivedChar.add_callback(self._console_incoming)
        scf.cf.appchannel.packet_received.add_callback(self._packet_received)

    def _set_params(self, scf: SyncCrazyflie):
        # TODO Pass values as config / update from UI
        scf.cf.param.set_value("app.updateTime", 2.0)
        scf.cf.param.set_value("app.defaultZ", 0.5)
        scf.cf.param.set_value("app.distanceTrigger", 0.3)

    def _connected(self, link_uri):
        print("Connected!")

    def _connection_failed(self, link_uri, msg):
        print("Connection to %s failed: %s" % (link_uri, msg))

    def _connection_lost(self, link_uri, msg):
        print("Connection to %s lost: %s" % (link_uri, msg))

    def _disconnected(self, link_uri):
        print("Disconnected from %s" % link_uri)

    def _console_incoming(self, console_text):
        print(console_text, end='')

    def _packet_received(self, data):
        (data,) = struct.unpack("<f", data)
        print(f"Received packet: {data}")

    def disconnect(self):
        self._swarm.close_links()

    def start_mission(self):
        self._swarm.parallel_safe(start_mission)

    def end_mission(self):
        self._swarm.parallel_safe(end_mission)

    def force_end_mission(self):
        self._swarm.parallel_safe(force_end_mission)

    def identify(self, uris):
        self._swarm.parallel_safe(identify, {uri: [uri in uris] for uri in self._swarm._cfs})

    def discover(self):
        available_devices = []
        for i in range(5):
            devices_on_address = cflib.crtp.scan_interfaces(self.base_uri + i)
            available_devices.extend(device[0] for device in devices_on_address)
        return available_devices
