import logging
import struct
import time
import cflib
from cflib.crazyflie import Crazyflie

logging.basicConfig(level=logging.ERROR)


class SwarmClient:
    Uris = [
        'radio://0/80/2M/E7E7E7E751',
        'radio://0/80/2M/E7E7E7E752'
    ]

    commands = {"identify": 0}

    def __init__(self, uri):
        cflib.crtp.init_drivers(enable_debug_driver=False)
        self._cf = Crazyflie()

        self._cf.connected.add_callback(self._connected)
        self._cf.disconnected.add_callback(self._disconnected)
        self._cf.connection_failed.add_callback(self._connection_failed)
        self._cf.connection_lost.add_callback(self._connection_lost)
        self._cf.console.receivedChar.add_callback(self._console_incoming)
        self._cf.appchannel.packet_received.add_callback(self._packet_received)

        self._cf.open_link(uri)

        print('Connecting to %s' % uri)

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
        (data, ) = struct.unpack("<f", data)
        print(f"Received packet: {data}")

    def _send_packet(self, packet):
        self._cf.appchannel.send_packet(packet)

    def identify(self):
        data = struct.pack("<d", self.commands["identify"])
        self._send_packet(data)
