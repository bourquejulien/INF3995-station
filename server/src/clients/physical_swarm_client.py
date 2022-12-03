import logging
from collections import deque

import cflib
import struct
from cflib import crtp
from cflib.crazyflie.swarm import CachedCfFactory, Swarm

from src.classes.events.log import generate_log
from src.classes.events.metric import generate_metric
from src.classes.position import Position
from src.classes.distance import Distance
from src.clients.drone_clients.physical_drone_client import identify, start_mission, end_mission, force_end_mission, \
    set_synchronization
from src.clients.abstract_swarm_client import AbstractSwarmClient

from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

from src.exceptions.custom_exception import CustomException
from src.exceptions.hardware_exception import HardwareException

logger = logging.getLogger(__name__)

RATE_LIMIT = "?rate_limit=100"


class MappingAdapter:
    _history: deque[(Position, Distance)]
    _average_size: int

    def __init__(self, average_size: int):
        self._history = deque()
        self._average_size = average_size

    def append(self, position: Position, distance: Distance):
        if len(self._history) >= self._average_size:
            self._history.pop()
        self._history.appendleft((position, distance))

    def clear(self):
        self._history.clear()

    def get_average(self):
        totalPosition = Position(0, 0, 0)
        totalDistance = Distance(0, 0, 0, 0)

        for position, distance in self._history:
            totalPosition = totalPosition + position
            totalDistance = totalDistance + distance

        return totalPosition * (1 / len(self._history)), totalDistance * (1 / len(self._history))

    def append_and_get(self, position, distance):
        self.append(position, distance)
        return self.get_average()


def _mapping_cast(position: Position, distance: Distance):
    front = distance.front
    back = distance.back
    left = distance.left
    right = distance.right
    x = position.y
    y = -position.x

    position_distances = []
    trigger = 10.0

    print(distance)

    if 0.01 < front < trigger:
        position_distances.append(Position(x, y + front, 0))
    if 0.01 < back < trigger:
        position_distances.append(Position(x, y - back, 0))
    if 0.01 < left < trigger:
        position_distances.append(Position(x - left, y, 0))
    if 0.01 < right < trigger:
        position_distances.append(Position(x + right, y, 0))

    return Position(x, y, position.z), position_distances


class PhysicalSwarmClient(AbstractSwarmClient):
    base_uri = 0xE7E7E7E750
    _mapping_adapter: MappingAdapter
    _is_sync_enabled: bool
    _swarm: Swarm | None

    def __init__(self, config):
        super().__init__()
        self._mapping_adapter = MappingAdapter(5)
        self._is_sync_enabled = False
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
        scf.cf.param.add_update_callback(group="deck", name="bcFlow2", cb=self._param_deck_flow)

    def _set_params(self, scf: SyncCrazyflie):
        scf.cf.param.set_value("app.updateTime", self.config['clients']['drones']['update_time'])
        scf.cf.param.set_value("app.defaultZ", self.config['clients']['drones']['default_z'])
        scf.cf.param.set_value("app.distanceTrigger", self.config['clients']['drones']['trigger_distance'])

    def _param_deck_flow(self, scf, value_str):
        try:
            int_value = int(value_str)
        except Exception as e:
            raise CustomException("Callback error: ", "expected an integer as string") from e

        if int_value != 0:
            logger.info("Deck is attached")
        else:
            raise HardwareException("Deck is not attached: ", "Check deck connection")

    def _connected(self, link_uri):
        logger.info("Connected to %s", link_uri)

    def _disconnected(self, link_uri):
        logger.info("Disconnected from %s", link_uri)

    def _connection_failed(self, link_uri, msg):
        logger.error("Connection to %s failed: %s", link_uri, msg)

    def _connection_lost(self, link_uri, msg):
        logger.warning("Connection to %s lost: %s", link_uri, msg)

    def _console_incoming(self, uri, console_text):
        log = generate_log('', console_text, "INFO", uri)
        self._callbacks["logging"](log)

    def _packet_received(self, uri: str, data):
        data_type, data = int.from_bytes(data[0:1], "little"), data[1:]

        match data_type:
            case 0:
                status = int.from_bytes(data[0:1], "little")
                position = Position(*struct.unpack("<fff", data[1:]))
                metric = generate_metric(position, self.status[status], uri)

                self._callbacks["metric"](metric)

            case 1:
                distance = Distance(*struct.unpack("<ffff", data[:16]))
                position = Position(*struct.unpack("<ff", data[16:24]), 0)
                print(f"position: {position}")

                yaw = struct.unpack("<f", data[24:])
                position, distance = self._mapping_adapter.append_and_get(position, distance)
                self._callbacks["mapping"](uri, *_mapping_cast(position, distance))

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
        self._swarm = None
        self._mapping_adapter.clear()

    def start_mission(self):
        self._swarm.parallel_safe(start_mission)

    def end_mission(self):
        self._swarm.parallel_safe(end_mission)

    def force_end_mission(self):
        self._swarm.parallel_safe(force_end_mission)

    def identify(self, uris):
        self._swarm.parallel_safe(identify, {uri: [uri in uris] for uri in self._swarm._cfs})

    def toggle_drone_synchronisation(self):
        self._is_sync_enabled = not self._is_sync_enabled
        self._swarm.parallel_safe(set_synchronization, {uri: [self._is_sync_enabled] for uri in self._swarm._cfs})

    def discover(self, with_limit: bool = True):
        error_code = "Crazyradio not found"
        if cflib.crtp.get_interfaces_status().get("radio") == error_code:
            raise CustomException(error_code, "Dongle is not attached")

        start = self.base_uri + int(self.config["clients"]["uri_start"])
        end = self.base_uri + int(self.config["clients"]["uri_end"])

        available_devices = []
        for i in range(start, end + 1):
            devices_on_address = cflib.crtp.scan_interfaces(i)
            available_devices.extend(device[0] for device in devices_on_address)
        return [f"{uri}{RATE_LIMIT}" if with_limit else uri for uri in available_devices]

    @property
    def uris(self):
        if self._swarm is None:
            return []
        return [str(key) for key in self._swarm._cfs.keys()]
