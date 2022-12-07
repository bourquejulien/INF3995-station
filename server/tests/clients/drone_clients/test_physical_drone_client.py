import pytest
from src.clients.drone_clients.physical_drone_client import _send_packet, \
        identify, start_mission, end_mission, return_to_base, \
        force_end_mission, set_synchronization


def test_send_packet(app, mocker):
    scf_mock = mocker.Mock()
    scf_mock.cf = mocker.Mock()
    scf_mock.cf.appchannel = mocker.Mock()

    _send_packet(scf_mock, 'test')

    scf_mock.cf.appchannel.send_packet.assert_called_once_with('test')


def test_identify_should_send(app, mocker):
    struct_mock = mocker.patch('src.clients.drone_clients.physical_drone_client.struct')
    scf_mock = mocker.Mock()
    send_packet_mock = mocker.patch('src.clients.drone_clients.physical_drone_client._send_packet')

    identify(scf_mock, True)

    struct_mock.pack.assert_called_once()
    send_packet_mock.assert_called_once()


def test_identify_should_not_send(app, mocker):
    struct_mock = mocker.patch('src.clients.drone_clients.physical_drone_client.struct')
    scf_mock = mocker.Mock()
    send_packet_mock = mocker.patch('src.clients.drone_clients.physical_drone_client._send_packet')

    identify(scf_mock, False)

    struct_mock.pack.assert_not_called()
    send_packet_mock.assert_not_called()


def test_start_mission(app, mocker):
    struct_mock = mocker.patch('src.clients.drone_clients.physical_drone_client.struct')
    scf_mock = mocker.Mock()
    send_packet_mock = mocker.patch('src.clients.drone_clients.physical_drone_client._send_packet')

    start_mission(scf_mock)

    struct_mock.pack.assert_called_once()
    send_packet_mock.assert_called_once()


def test_end_mission(app, mocker):
    struct_mock = mocker.patch('src.clients.drone_clients.physical_drone_client.struct')
    scf_mock = mocker.Mock()
    send_packet_mock = mocker.patch('src.clients.drone_clients.physical_drone_client._send_packet')

    end_mission(scf_mock)

    struct_mock.pack.assert_called_once()
    send_packet_mock.assert_called_once()


def test_return_to_base(app, mocker):
    struct_mock = mocker.patch('src.clients.drone_clients.physical_drone_client.struct')
    scf_mock = mocker.Mock()
    send_packet_mock = mocker.patch('src.clients.drone_clients.physical_drone_client._send_packet')

    return_to_base(scf_mock)

    struct_mock.pack.assert_called_once()
    send_packet_mock.assert_called_once()


def test_force_end_mission(app, mocker):
    struct_mock = mocker.patch('src.clients.drone_clients.physical_drone_client.struct')
    scf_mock = mocker.Mock()
    send_packet_mock = mocker.patch('src.clients.drone_clients.physical_drone_client._send_packet')

    force_end_mission(scf_mock)

    struct_mock.pack.assert_called_once()
    send_packet_mock.assert_called_once()


def test_set_synchronization(app, mocker):
    scf_mock = mocker.Mock()
    scf_mock.cf = mocker.Mock()
    scf_mock.cf.param = mocker.Mock()

    set_synchronization(scf_mock, True)

    scf_mock.cf.param.set_value.assert_called_once_with('app.sync_enabled', True)
