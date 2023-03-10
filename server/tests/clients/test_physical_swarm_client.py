import types

import pytest
import struct

from freezegun import freeze_time

import src.clients.physical_swarm_client
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
    mocker.patch("src.clients.physical_swarm_client.crtp")
    swarm_client = PhysicalSwarmClient({})

    swarm_client._swarm = types.SimpleNamespace()
    swarm_client._base_return_syncer = types.SimpleNamespace()
    swarm_client._base_return_syncer.close = mocker.stub()
    swarm_client._base_return_syncer.remove_uri = mocker.stub()
    swarm_client._base_return_syncer.release = mocker.stub()
    swarm_client._swarm.close_links = mocker.stub()

    yield swarm_client


@pytest.fixture()
def logger_mock(mocker):
    mock = mocker.Mock()
    src.clients.physical_swarm_client.logger = mock
    yield mock


def test_connect(app, mocker, swarm_client):
    uris = ["test"]
    swarm_mock = mocker.Mock(Swarm)
    mocker.patch("src.clients.physical_swarm_client.Swarm", return_value=swarm_mock)
    swarm_mock.parallel_safe = mocker.stub()
    swarm_mock.open_links = mocker.stub()

    swarm_mock._cfs = {}

    swarm_client.connect(uris)

    swarm_mock.parallel_safe.assert_called()
    swarm_mock.open_links.assert_called_once()


def test_enable_callbacks(app, mocker, swarm_client):
    scf_mock = mocker.patch("cflib.crazyflie.syncCrazyflie.SyncCrazyflie")
    scf_mock.cf = mocker.patch("cflib.crazyflie.Crazyflie")
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


def test_param_deck_flow_with_true_int(app, mocker, swarm_client, logger_mock):
    scf_mock = mocker.stub()

    swarm_client._param_deck_flow(scf_mock, "1")

    logger_mock.info.assert_called_once_with("Deck is attached")


def test_param_deck_flow_with_false_int(app, mocker, swarm_client):
    error = ""
    scf_mock = mocker.stub()

    try:
        swarm_client._param_deck_flow(scf_mock, "0")
    except Exception as e:
        error = e

    assert error.__class__ == HardwareException
    assert error.name == "Deck is not attached: "
    assert error.message == "Check deck connection"


def test_param_deck_flow_with_invalid_string(app, mocker, swarm_client):
    error = ""
    scf_mock = mocker.stub()

    try:
        swarm_client._param_deck_flow(scf_mock, "test")
    except Exception as e:
        error = e

    assert error.__class__ == CustomException
    assert error.name == "Callback error: "
    assert error.message == "expected an integer as string"


def test_connected_callback(app, mocker, swarm_client, logger_mock):
    swarm_client._connected("test")
    logger_mock.info.assert_called_once_with("Connected to %s", "test")


def test_connection_failed_callback(app, mocker, swarm_client, logger_mock):
    swarm_client._connection_failed("test", "message")
    logger_mock.error.assert_called_once_with("Connection to %s failed: %s", "test", "message")


def test_connection_lost_callback(app, mocker, swarm_client, logger_mock):
    swarm_client._connection_lost("test", "message")
    logger_mock.warning.assert_called_once_with("Connection to %s lost: %s", "test", "message")


def test_disconnected_callback(app, mocker, swarm_client, logger_mock):
    swarm_client._disconnected("test")
    logger_mock.info.assert_called_once_with("Disconnected from %s", "test")


@freeze_time("2022-01-01")
def test_console_incoming_callback(app, mocker, swarm_client):
    generated_logs = []
    swarm_client._callbacks = {"logging": lambda x: generated_logs.append(x)}
    log = generate_log("", "test", "INFO", "1")
    swarm_client._console_incoming("1", "test")
    assert log == generated_logs[0]


@freeze_time("2022-01-01")
def test_packet_received_callback(app, mocker, swarm_client):
    param = struct.pack("<ccffff", b"\x00", b"\x00", 2, 2.5, 3, 3.5)
    generated_metrics = []
    swarm_client._callbacks = {"metric": lambda x: generated_metrics.append(x)}
    stub = types.SimpleNamespace()
    stub.adapt = lambda x: x
    swarm_client._position_adapters = {"abc": stub}
    swarm_client._packet_received("abc", param)
    assert generate_metric(Position(2.0, 2.5, 3.0), "Idle", "abc", battery_level=3.5) == generated_metrics[0]


def test_disconnect(app, swarm_client):
    stub = swarm_client._swarm.close_links
    swarm_client.disconnect()
    stub.assert_called_once()


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
    uris = ["test1", "test2"]
    swarm_client._swarm = types.SimpleNamespace()
    swarm_client._swarm._cfs = ["test2"]
    swarm_client._swarm.parallel_safe = mocker.stub()

    swarm_client.identify(uris)

    swarm_client._swarm.parallel_safe.assert_called_once_with(identify, {"test2": [True]})


def test_discover(app, mocker, swarm_client):
    scan_interfaces_mock = mocker.patch("cflib.crtp.scan_interfaces", return_value=[["test"]])
    swarm_client.config = {"clients": {"uri_start": 0, "uri_end": 2}}

    base = swarm_client.base_uri
    calls = [mocker.call(base), mocker.call(base + 1), mocker.call(base + 2)]

    return_value = swarm_client.discover()

    scan_interfaces_mock.assert_has_calls(calls)
    assert return_value == ["test?rate_limit=100"] * 3
