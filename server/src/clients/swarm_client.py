import logging
import struct
import time

import cflib
from cflib import crtp
from cflib.crazyflie import Crazyflie

from src.clients.drone_client import DroneClient

logging.basicConfig(level=logging.ERROR)


class SwarmClient(DroneClient):
    base_uri = 0xE7E7E7E750

    commands = {"identify": 0}

    def __init__(self):
        crtp.init_drivers(enable_debug_driver=False)
        self._cf = Crazyflie()

        self._cf.connected.add_callback(self._connected)
        self._cf.disconnected.add_callback(self._disconnected)
        self._cf.connection_failed.add_callback(self._connection_failed)
        self._cf.connection_lost.add_callback(self._connection_lost)
        self._cf.console.receivedChar.add_callback(self._console_incoming)
        self._cf.appchannel.packet_received.add_callback(self._packet_received)

    def _connected(self, link_uri):
        print("Connected!")

    def _connection_failed(self, link_uri, msg):
        print('Connection to %s failed: %s' % (link_uri, msg))

    def _connection_lost(self, link_uri, msg):
        print('Connection to %s lost: %s' % (link_uri, msg))

    def _disconnected(self, link_uri):
        print('Disconnected from %s' % link_uri)

    def _console_incoming(self, console_text):
        print(console_text, end='')

    def _packet_received(self, data):
        (data,) = struct.unpack("<f", data)
        print(f"Received packet: {data}")

    def _send_packet(self, packet):
        self._cf.appchannel.send_packet(packet)

    def connect(self, uri):
        self._cf.open_link(uri)
        print('Connecting to %s' % uri)

    def disconnect(self):
        self._cf.close_link()

    def identify(self):
        data = struct.pack("<d", self.commands["identify"])
        self._send_packet(data)

    def start_mission(self):
        pass

    def end_mission(self):
        pass

    def discover(self):
        available_devices = []
        for i in range(5):
            devices_on_address = cflib.crtp.scan_interfaces(self.base_uri + i)
            available_devices.extend(device[0] for device in devices_on_address)
        return available_devices


# client = SwarmClient()
# client.connect(client.discover()[0])
#
# client.identify()
# time.sleep(1)
# client.disconnect()
#
