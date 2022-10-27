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
        uri = scf.cf.link_uri
        scf.cf.connected.add_callback(self._connected)
        scf.cf.disconnected.add_callback(self._disconnected)
        scf.cf.connection_failed.add_callback(self._connection_failed)
        scf.cf.connection_lost.add_callback(self._connection_lost)
        scf.cf.console.receivedChar.add_callback(lambda data: self._console_incoming(uri, data))
        scf.cf.appchannel.packet_received.add_callback(lambda text: self._packet_received(uri, text))
        scf.cf.param.add_update_callback(group="deck", name="bcFlow2", cb=self.param_deck_flow)

    def _set_params(self, scf: SyncCrazyflie):
        # TODO Pass values as config / update from UI
        scf.cf.param.set_value("app.updateTime", 2.0)
        scf.cf.param.set_value("app.defaultZ", 0.5)
        scf.cf.param.set_value("app.distanceTrigger", 0.3)

    def param_deck_flow(self, scf, value_str):
        try:
            int_value = int(value_str)
        except Exception as e:
            raise CustomException('Callback error: ', 'expected an integer as string') from e

        if int_value != 0:
            print('Deck is attached')
        else:
            raise HardwareException('Deck is not attached: ', 'Check deck connection')

    def _connected(self, link_uri):
        print("Connected to %s" % (link_uri))

    def _connection_failed(self, link_uri, msg):
        print("Connection to %s failed: %s" % (link_uri, msg))

    def _connection_lost(self, link_uri, msg):
        print("Connection to %s lost: %s" % (link_uri, msg))

    def _disconnected(self, link_uri):
        print("Disconnected from %s" % link_uri)

    def _console_incoming(self, uri, console_text):
        log = generate_log('', console_text, "INFO", uri)
        print(log)

    def _packet_received(self, uri: str, data):
        data_type, data = data[0], data[1:]

        match data_type:
            case 0:
                status = data[0]
                position = Position(*struct.unpack("<fff", data[1:]))
                metric = generate_metric(position, status, uri)

                print(metric)

            case 1:
                distance = Distance(*struct.unpack("<ffffff", data))
                print(distance)

            case _:
                raise CustomException("Unpack error: ", f"Unknown data type: {data_type}")

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

    def get_position(self):
        return
