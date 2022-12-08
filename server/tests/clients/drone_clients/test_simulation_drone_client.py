import pytest
import grpc
from src.clients.drone_clients.simulation_drone_client import SimulationDroneClient
from src.exceptions.custom_exception import CustomException


@pytest.fixture()
def drone_client(mocker):
    yield SimulationDroneClient("host", 6666)


def test_is_ready(app, mocker, drone_client):
    drone_client._channel = "test"
    grpc_mock = mocker.patch("src.clients.drone_clients.simulation_drone_client.grpc")
    return_mock = mocker.Mock()
    return_mock.result.return_value = ""
    grpc_mock.channel_ready_future.return_value = return_mock

    result = drone_client.is_ready(0)

    grpc_mock.channel_ready_future.assert_called_once_with("test")
    assert result


def test_is_ready_error(app, mocker, drone_client):
    drone_client._channel = "test"
    grpc_mock = mocker.patch("src.clients.drone_clients.simulation_drone_client.grpc")
    grpc_mock.channel_ready_future.side_effect = grpc.FutureTimeoutError()

    result = drone_client.is_ready(0)

    grpc_mock.channel_ready_future.assert_called_once_with("test")
    assert not result


def test_connect(app, mocker, drone_client):
    drone_client._address = "test"
    grpc_mock = mocker.patch("src.clients.drone_clients.simulation_drone_client.grpc")
    grpc_mock.insecure_channel.return_value = "test"
    simulation_pb2_mock = mocker.patch("src.clients.drone_clients.simulation_drone_client.simulation_pb2_grpc")
    simulation_pb2_mock.SimulationStub.return_value = "test"

    drone_client.connect()

    grpc_mock.insecure_channel.assert_called_once_with("test")
    assert drone_client._channel == "test"
    assert drone_client._stub == "test"


def test_disconnect(app, mocker, drone_client):
    channel_mock = mocker.Mock()
    drone_client._channel = channel_mock

    drone_client.disconnect()

    channel_mock.close.assert_called_once()


def test_start_mission(app, mocker, drone_client):
    drone_client.uri = "test"
    drone_client._stub = mocker.Mock()
    simulation_pb2_mock = mocker.patch("src.clients.drone_clients.simulation_drone_client.simulation_pb2")

    drone_client.start_mission()

    drone_client._stub.StartMission.assert_called_once()
    simulation_pb2_mock.MissionRequest.assert_called_once_with(uri="test")


def test_start_mission_error(app, mocker, drone_client):
    drone_client.uri = "test"
    drone_client._stub = mocker.Mock()
    simulation_pb2_mock = mocker.patch("src.clients.drone_clients.simulation_drone_client.simulation_pb2")
    error = grpc.RpcError()
    error.code = lambda: grpc.StatusCode.INVALID_ARGUMENT
    simulation_pb2_mock.MissionRequest.side_effect = error

    try:
        drone_client.start_mission()
    except CustomException as e:
        assert e.name == "RPCError: "

    simulation_pb2_mock.MissionRequest.assert_called_once_with(uri="test")


def test_end_mission(app, mocker, drone_client):
    drone_client.uri = "test"
    drone_client._stub = mocker.Mock()
    simulation_pb2_mock = mocker.patch("src.clients.drone_clients.simulation_drone_client.simulation_pb2")

    drone_client.end_mission()

    drone_client._stub.EndMission.assert_called_once()
    simulation_pb2_mock.MissionRequest.assert_called_once_with(uri="test")


def test_end_mission_error(app, mocker, drone_client):
    drone_client.uri = "test"
    drone_client._stub = mocker.Mock()
    simulation_pb2_mock = mocker.patch("src.clients.drone_clients.simulation_drone_client.simulation_pb2")
    error = grpc.RpcError()
    error.code = lambda: grpc.StatusCode.INVALID_ARGUMENT
    simulation_pb2_mock.MissionRequest.side_effect = error

    try:
        drone_client.end_mission()
    except CustomException as e:
        assert e.name == "RPCError: "

    simulation_pb2_mock.MissionRequest.assert_called_once_with(uri="test")


def test_force_end_mission(app, mocker, drone_client):
    drone_client.uri = "test"
    drone_client._stub = mocker.Mock()
    simulation_pb2_mock = mocker.patch("src.clients.drone_clients.simulation_drone_client.simulation_pb2")

    drone_client.force_end_mission()

    drone_client._stub.EndMission.assert_called_once()
    simulation_pb2_mock.MissionRequest.assert_called_once_with(uri="test")


def test_force_end_mission_error(app, mocker, drone_client):
    drone_client.uri = "test"
    drone_client._stub = mocker.Mock()
    simulation_pb2_mock = mocker.patch("src.clients.drone_clients.simulation_drone_client.simulation_pb2")
    error = grpc.RpcError()
    error.code = lambda: grpc.StatusCode.INVALID_ARGUMENT
    simulation_pb2_mock.MissionRequest.side_effect = error

    try:
        drone_client.force_end_mission()
    except CustomException as e:
        assert e.name == "RPCError: "

    simulation_pb2_mock.MissionRequest.assert_called_once_with(uri="test")


def test_return_to_base(app, mocker, drone_client):
    drone_client.uri = "test"
    drone_client._stub = mocker.Mock()
    simulation_pb2_mock = mocker.patch("src.clients.drone_clients.simulation_drone_client.simulation_pb2")

    drone_client.return_to_base()

    drone_client._stub.ReturnToBase.assert_called_once()
    simulation_pb2_mock.MissionRequest.assert_called_once_with(uri="test")


def test_end_mission_error(app, mocker, drone_client):
    drone_client.uri = "test"
    drone_client._stub = mocker.Mock()
    simulation_pb2_mock = mocker.patch("src.clients.drone_clients.simulation_drone_client.simulation_pb2")
    error = grpc.RpcError()
    error.code = lambda: grpc.StatusCode.INVALID_ARGUMENT
    simulation_pb2_mock.MissionRequest.side_effect = error

    try:
        drone_client.return_to_base()
    except CustomException as e:
        assert e.name == "RPCError: "

    simulation_pb2_mock.MissionRequest.assert_called_once_with(uri="test")


def test_get_telemetrics(app, mocker, drone_client):
    drone_client.uri = "test"
    drone_client._stub = mocker.Mock()
    simulation_pb2_mock = mocker.patch("src.clients.drone_clients.simulation_drone_client.simulation_pb2")

    drone_client.get_telemetrics()

    drone_client._stub.GetTelemetrics.assert_called_once()
    simulation_pb2_mock.MissionRequest.assert_called_once_with(uri="test")


def test_get_telemetrics_error(app, mocker, drone_client):
    drone_client.uri = "test"
    drone_client._stub = mocker.Mock()
    simulation_pb2_mock = mocker.patch("src.clients.drone_clients.simulation_drone_client.simulation_pb2")
    error = grpc.RpcError()
    error.code = lambda: grpc.StatusCode.INVALID_ARGUMENT
    simulation_pb2_mock.MissionRequest.side_effect = error

    try:
        drone_client.get_telemetrics()
    except CustomException as e:
        assert e.name == "RPCError: "

    simulation_pb2_mock.MissionRequest.assert_called_once_with(uri="test")


def test_get_distances(app, mocker, drone_client):
    drone_client.uri = "test"
    drone_client._stub = mocker.Mock()
    simulation_pb2_mock = mocker.patch("src.clients.drone_clients.simulation_drone_client.simulation_pb2")

    drone_client.get_distances()

    drone_client._stub.GetDistances.assert_called_once()
    simulation_pb2_mock.MissionRequest.assert_called_once_with(uri="test")


def test_get_distances_error(app, mocker, drone_client):
    drone_client.uri = "test"
    drone_client._stub = mocker.Mock()
    simulation_pb2_mock = mocker.patch("src.clients.drone_clients.simulation_drone_client.simulation_pb2")
    error = grpc.RpcError()
    error.code = lambda: grpc.StatusCode.INVALID_ARGUMENT
    simulation_pb2_mock.MissionRequest.side_effect = error

    try:
        drone_client.get_distances()
    except CustomException as e:
        assert e.name == "RPCError: "

    simulation_pb2_mock.MissionRequest.assert_called_once_with(uri="test")


def test_get_logs(app, mocker, drone_client):
    drone_client.uri = "test"
    drone_client._stub = mocker.Mock()
    simulation_pb2_mock = mocker.patch("src.clients.drone_clients.simulation_drone_client.simulation_pb2")

    drone_client.get_logs()

    drone_client._stub.GetLogs.assert_called_once()
    simulation_pb2_mock.MissionRequest.assert_called_once_with(uri="test")


def test_get_distances_error(app, mocker, drone_client):
    drone_client.uri = "test"
    drone_client._stub = mocker.Mock()
    simulation_pb2_mock = mocker.patch("src.clients.drone_clients.simulation_drone_client.simulation_pb2")
    error = grpc.RpcError()
    error.code = lambda: grpc.StatusCode.INVALID_ARGUMENT
    simulation_pb2_mock.MissionRequest.side_effect = error

    try:
        drone_client.get_logs()
    except CustomException as e:
        assert e.name == "RPCError: "

    simulation_pb2_mock.MissionRequest.assert_called_once_with(uri="test")
