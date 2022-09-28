import struct

from cflib.crazyflie import Crazyflie
from cflib import crtp

from src.clients.drone_clients.drone_client import DroneClient


class PhyDroneClient(DroneClient):
    commands = {"identify": 0}

    def __init__(self, uri):
        crtp.init_drivers(enable_debug_driver=False)
        self._cf = Crazyflie()
        self.uri = uri

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

    def connect(self):
        self._cf.open_link(self.uri)
        print('Connecting to %s' % self.uri)

    def disconnect(self):
        self._cf.close_link()

    def identify(self):
        data = struct.pack("<d", self.commands["identify"])
        self._send_packet(data)

    def start_mission(self):
        pass

    def end_mission(self):
        pass
