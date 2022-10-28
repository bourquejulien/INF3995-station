import types
from datetime import date

import pytest
import struct

from src.classes.events.log import generate_log
from src.classes.events.metric import generate_metric
from src.classes.position import Position
from src.clients.physical_swarm_client import PhysicalSwarmClient
from src.exceptions.hardware_exception import HardwareException
from src.exceptions.custom_exception import CustomException
from cflib.crazyflie.swarm import Swarm
from src.clients.drone_clients.physical_drone_client import identify, start_mission, end_mission


@pytest.fixture()
def swarm_client(mocker):
    mocker.patch('src.clients.physical_swarm_client.crtp')
    yield PhysicalSwarmClient()


@pytest.fixture()
def print_mock(mocker):
    yield mocker.patch('src.clients.physical_swarm_client.print')


@pytest.fixture()
def time_mock(mocker):
    mock_time = mocker.patch('src.classes.events.log.get_timestamp_ms', return_value=100)

    yield mock_time


def test_connect(app, mocker, swarm_client):
    uris = ['test']
    swarm_mock = mocker.Mock(Swarm)
    mocker.patch('src.clients.physical_swarm_client.Swarm', return_value=swarm_mock)
    swarm_mock.parallel_safe = mocker.stub()
    swarm_mock.open_links = mocker.stub()

    swarm_client.connect(uris)

    swarm_mock.parallel_safe.assert_called()
    swarm_mock.open_links.assert_called_once()


def test_enable_callbacks(app, mocker, swarm_client):
    scf_mock = mocker.patch('cflib.crazyflie.syncCrazyflie.SyncCrazyflie')
    scf_mock.cf = mocker.patch('cflib.crazyflie.Crazyflie')
    scf_mock.cf.connected.add_callback = mocker.stub()
    scf_mock.cf.disconnected.add_callback = mocker.stub()
    scf_mock.cf.connection_failed.add_callback = mocker.stub()
    scf_mock.cf.connection_lost.add_callback = mocker.stub()
    scf_mock.cf.console.receivedChar.add_callback = mocker.stub()
    scf_mock.cf.appchannel.packet_received.add_callback = mocker.stub()
    scf_mock.cf.param.add_update_callback = mocker.stub()

    swarm_client._enable_callbacks(scf_mock)

    scf_mock.cf.connected.add_callback.assert_called_once()
    scf_mock.cf.disconnected.add_callback.assert_called_once()
    scf_mock.cf.connection_failed.add_callback.assert_called_once()
    scf_mock.cf.connection_lost.add_callback.assert_called_once()
    scf_mock.cf.console.receivedChar.add_callback.assert_called_once()
    scf_mock.cf.appchannel.packet_received.add_callback.assert_called_once()
    scf_mock.cf.param.add_update_callback.assert_called_once()


def test_param_deck_flow_with_true_int(app, mocker, swarm_client, print_mock):
    scf_mock = mocker.stub()

    swarm_client.param_deck_flow(scf_mock, '1')

    print_mock.assert_called_once_with('Deck is attached')


def test_param_deck_flow_with_false_int(app, mocker, swarm_client):
    error = ''
    scf_mock = mocker.stub()

    try:
        swarm_client.param_deck_flow(scf_mock, '0')
    except Exception as e:
        error = e

    assert error.__class__ == HardwareException
    assert error.name == 'Deck is not attached: '
    assert error.message == 'Check deck connection'


def test_param_deck_flow_with_invalid_string(app, mocker, swarm_client):
    error = ''
    scf_mock = mocker.stub()

    try:
        swarm_client.param_deck_flow(scf_mock, 'test')
    except Exception as e:
        error = e

    assert error.__class__ == CustomException
    assert error.name == 'Callback error: '
    assert error.message == 'expected an integer as string'


def test_connected_callback(app, mocker, swarm_client, print_mock):
    swarm_client._connected('test')

    print_mock.assert_called_once_with('Connected to test')


def test_connection_failed_callback(app, mocker, swarm_client, print_mock):
    swarm_client._connection_failed('test', 'message')

    print_mock.assert_called_once_with('Connection to test failed: message')


def test_connection_lost_callback(app, mocker, swarm_client, print_mock):
    swarm_client._connection_lost('test', 'message')

    print_mock.assert_called_once_with('Connection to test lost: message')


def test_disconnected_callback(app, mocker, swarm_client, print_mock):
    swarm_client._disconnected('test')

    print_mock.assert_called_once_with('Disconnected from test')


def test_console_incoming_callback(app, mocker, swarm_client, print_mock):
    swarm_client._console_incoming('1', 'test')
    print_mock.assert_called_once()
    # TODO
    # print_mock.assert_called_once_with(generate_log('', 'test', 'INFO', '1'))


def test_packet_received_callback(app, mocker, swarm_client, print_mock):
    param = struct.pack('<ccfff', b'0', b'0', 2, 2.5, 3)
    swarm_client._packet_received('abc', param)
    print_mock.assert_called_once_with(generate_metric(Position(2, 2.5, 3), 'Identify', 'abc'))


def test_disconnect(app, mocker, swarm_client):
    swarm_client._swarm = types.SimpleNamespace()
    swarm_client._swarm.close_links = mocker.stub()

    swarm_client.disconnect()

    swarm_client._swarm.close_links.assert_called_once()


def test_start_mission(app, mocker, swarm_client):
    swarm_client._swarm = types.SimpleNamespace()
    swarm_client._swarm.parallel_safe = mocker.stub()

    swarm_client.start_mission()

    swarm_client._swarm.parallel_safe.assert_called_once_with(start_mission)


def test_end_mission(app, mocker, swarm_client):
    swarm_client._swarm = types.SimpleNamespace()
    swarm_client._swarm.parallel_safe = mocker.stub()

    swarm_client.end_mission()

    swarm_client._swarm.parallel_safe.assert_called_once_with(end_mission)


def test_identify(app, mocker, swarm_client):
    uris = ['test1', 'test2']
    swarm_client._swarm = types.SimpleNamespace()
    swarm_client._swarm._cfs = ['test2']
    swarm_client._swarm.parallel_safe = mocker.stub()

    swarm_client.identify(uris)

    swarm_client._swarm.parallel_safe.assert_called_once_with(identify, {'test2': [True]})


def test_discover(app, mocker, swarm_client):
    scan_interfaces_mock = mocker.patch('cflib.crtp.scan_interfaces', return_value=[['test']])
    base = swarm_client.base_uri
    calls = [mocker.call(base), mocker.call(base + 1),
             mocker.call(base + 2), mocker.call(base + 3),
             mocker.call(base + 4)]

    return_value = swarm_client.discover()

    scan_interfaces_mock.assert_has_calls(calls)
    assert return_value == ['test', 'test', 'test', 'test', 'test']
