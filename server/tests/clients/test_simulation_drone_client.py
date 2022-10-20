import pytest
from src.clients.simulation_swarm_client import SimulationSwarmClient
from src.clients.drone_clients.simulation_drone_client import SimulationDroneClient
from src.exceptions.hardware_exception import HardwareException
from src.exceptions.custom_exception import CustomException


@pytest.fixture()
def swarm_client(mocker):
    config = {'argos': {'port': 0, 'hostname': 'host'}}
    yield SimulationSwarmClient(config)


def test_start_mission(app, mocker, swarm_client):
    drone_mock = mocker.Mock(SimulationDroneClient)
    swarm_client._drone_clients = [drone_mock, drone_mock, drone_mock]
    calls = [mocker.call(), mocker.call(), mocker.call()]

    swarm_client.start_mission()

    drone_mock.start_mission.assert_has_calls(calls)


def test_end_mission(app, mocker, swarm_client):
    drone_mock = mocker.Mock(SimulationDroneClient)
    swarm_client._drone_clients = [drone_mock, drone_mock, drone_mock]
    calls = [mocker.call(), mocker.call(), mocker.call()]

    swarm_client.end_mission()

    drone_mock.end_mission.assert_has_calls(calls)
