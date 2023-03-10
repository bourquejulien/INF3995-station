import struct
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

commands = {"identify": 0, "start_mission": 1, "end_mission": 2, "force_end_mission": 3, "return_to_base": 4}


def _send_packet(scf: SyncCrazyflie, packet):
    scf.cf.appchannel.send_packet(packet)


def identify(scf: SyncCrazyflie, should_send):
    if should_send:
        data = struct.pack("<i", commands["identify"])
        _send_packet(scf, data)


def start_mission(scf: SyncCrazyflie):
    data = struct.pack("<i8sf", commands["start_mission"], b"", 0.2)
    _send_packet(scf, data)


def end_mission(scf: SyncCrazyflie):
    data = struct.pack("<i", commands["end_mission"])
    _send_packet(scf, data)


def return_to_base(scf: SyncCrazyflie):
    data = struct.pack("<i", commands["return_to_base"])
    _send_packet(scf, data)


def force_end_mission(scf: SyncCrazyflie):
    data = struct.pack("<i", commands["force_end_mission"])
    _send_packet(scf, data)


def set_synchronization(scf: SyncCrazyflie, value: bool):
    scf.cf.param.set_value("app.sync_enabled", value)


def get_position():
    return
