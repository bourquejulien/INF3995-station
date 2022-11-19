import logging

import cflib
import struct
from cflib import crtp
from cflib.crazyflie.swarm import CachedCfFactory, Swarm

from src.classes.events.log import generate_log
from src.classes.events.metric import generate_metric
from src.classes.position import Position
from src.classes.distance import Distance
from src.clients.drone_clients.physical_drone_client import identify, start_mission, end_mission, force_end_mission
from src.clients.abstract_swarm_client import AbstractSwarmClient

from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

from src.exceptions.custom_exception import CustomException
from src.exceptions.hardware_exception import HardwareException

logging.basicConfig(level=logging.ERROR)


class PhysicalSwarmClient(AbstractSwarmClient):
    base_uri = 0xE7E7E7E750
    _swarm: Swarm | None

    def __init__(self, config):
        super().__init__()
        self._swarm = None
        self._factory = CachedCfFactory(rw_cache="./cache")
        crtp.init_drivers(enable_debug_driver=False)
        self.config = config

    def _enable_callbacks(self, scf: SyncCrazyflie):
        uri = scf.cf.link_uri
        scf.cf.connected.add_callback(self._connected)
        scf.cf.disconnected.add_callback(self._disconnected)
        scf.cf.connection_failed.add_callback(self._connection_failed)
        scf.cf.connection_lost.add_callback(self._connection_lost)
        scf.cf.console.receivedChar.add_callback(lambda data: self._console_incoming(uri, data))
        scf.cf.appchannel.packet_received.add_callback(lambda text: self._packet_received(uri, text))
        scf.cf.param.add_update_callback(group="deck", name="bcFlow2", cb=self.param_deck_flow)

    def _set_params(self, scf: SyncCrazyflie):
        scf.cf.param.set_value("app.updateTime", self.config['clients']['drones']['update_time'])
        scf.cf.param.set_value("app.defaultZ", self.config['clients']['drones']['default_z'])
        scf.cf.param.set_value("app.distanceTrigger", self.config['clients']['drones']['trigger_distance'])

    def param_deck_flow(self, scf, value_str):
        try:
            int_value = int(value_str)
        except Exception as e:
            raise CustomException("Callback error: ", "expected an integer as string") from e

        if int_value != 0:
            print("Deck is attached")
        else:
            raise HardwareException("Deck is not attached: ", "Check deck connection")

    def _connected(self, link_uri):
        print(f"Connected to {link_uri}")

    def _connection_failed(self, link_uri, msg):
        print(f"Connection to {link_uri} failed: {msg}")

    def _connection_lost(self, link_uri, msg):
        print(f"Connection to {link_uri} lost: {msg}")

    def _disconnected(self, link_uri):
        print(f"Disconnected from {link_uri}")

    def _console_incoming(self, uri, console_text):
        log = generate_log('', console_text, "INFO", uri)
        self._callbacks["logging"](log)

    def _packet_received(self, uri: str, data):
        data_type, data = int.from_bytes(data[0:1], "little"), data[1:]

        match data_type:
            case 0:
                status = int.from_bytes(data[0:1], "little")
                position = Position(*struct.unpack("<fff", data[1:]))
                metric = generate_metric(position, self.STATUS[status], uri)

                self._callbacks["metric"](metric)

            case 1:
                distance = Distance(*struct.unpack("<ffff", data[:16]))
                position = Position(*struct.unpack("<fff", data[16:]))
                self._callbacks["mapping"](uri, position, distance)

            case _:
                raise CustomException("Unpack error: ", f"Unknown data type: {data_type}")

    def connect(self, uris):
        self._swarm = Swarm(uris, factory=self._factory)
        self._swarm.open_links()
        self._swarm.parallel_safe(self._enable_callbacks)
        self._swarm.parallel_safe(self._set_params)

    def disconnect(self):
        if self._swarm is not None:
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
        error_code = "Crazyradio not found"
        if cflib.crtp.get_interfaces_status().get("radio") == error_code:
            raise CustomException(error_code, "Dongle is not attached")

        available_devices = []
        for i in range(5):
            devices_on_address = cflib.crtp.scan_interfaces(self.base_uri + i)
            available_devices.extend(device[0] for device in devices_on_address)
        return available_devices

    @property
    def uris(self):
        return self._swarm._cfs.keys()
