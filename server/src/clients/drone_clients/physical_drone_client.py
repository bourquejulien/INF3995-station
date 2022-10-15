import struct

from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

commands = {"identify": 0, "start_mission": 1, "end_mission": 2}

command_packet = {
    "command_id": 0,
    "command_param_name": "",
    "command_param_value": 0.0
}


def _send_packet(scf: SyncCrazyflie, packet):
    scf.cf.appchannel.send_packet(packet)


def identify(scf: SyncCrazyflie, should_send):
    if should_send:
        data = struct.pack("<i", commands["identify"])
        _send_packet(scf, data)


def start_mission(scf: SyncCrazyflie):
    data = struct.pack("<i8sf", commands["start_mission"], b"", 0.5)
    _send_packet(scf, data)


def end_mission(scf: SyncCrazyflie):
    data = struct.pack("<i", commands["end_mission"])
    _send_packet(scf, data)
