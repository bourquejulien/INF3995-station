import struct

from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

commands = {"identify": 0}


def _send_packet(scf: SyncCrazyflie, packet):
    scf.cf.appchannel.send_packet(packet)


def identify(scf: SyncCrazyflie, should_send):
    if should_send:
        data = struct.pack("<d", commands["identify"])
        _send_packet(scf, data)


def start_mission(scf: SyncCrazyflie):
    pass


def end_mission(scf: SyncCrazyflie):
    pass
