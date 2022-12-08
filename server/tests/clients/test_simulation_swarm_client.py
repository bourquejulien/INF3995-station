import pytest
from src.classes.position import Position
from src.clients.simulation_swarm_client \
        import SimulationSwarmClient, distance_to_position
from src.clients.drone_clients.simulation_drone_client \
        import SimulationDroneClient
from src.exceptions.custom_exception import CustomException


@pytest.fixture()
def swarm_client(mocker):
    config = {'argos': {'port': 0, 'hostname': 'host'}}
    yield SimulationSwarmClient(config)


def test_distance_to_position(app, mocker):
    distance_mock = mocker.Mock()
    distance_mock.front = 1
    distance_mock.back = 2
    distance_mock.left = 3
    distance_mock.right = 4
    distance_mock.position.x = 1
    distance_mock.position.y = 2

    result = distance_to_position(distance_mock)

    assert result == [
            Position(1, 1.99, 0),
            Position(1, 2.02, 0),
            Position(1.03, 2, 0),
            Position(0.96, 2, 0)
        ]


def test_start_mission(app, mocker, swarm_client):
    drone_mock = mocker.Mock(SimulationDroneClient)
    swarm_client._drone_clients = {"1": drone_mock, "2": drone_mock, "3": drone_mock}
    calls = [mocker.call(), mocker.call(), mocker.call()]

    swarm_client.start_mission()

    drone_mock.start_mission.assert_has_calls(calls)


def test_end_mission(app, mocker, swarm_client):
    drone_mock = mocker.Mock(SimulationDroneClient)
    swarm_client._drone_clients= {"1": drone_mock, "2": drone_mock, "3": drone_mock}
    calls = [mocker.call(), mocker.call(), mocker.call()]

    swarm_client.end_mission()

    drone_mock.end_mission.assert_has_calls(calls)


def test_force_end_mission(app, mocker, swarm_client):
    drone_mock = mocker.Mock(SimulationDroneClient)
    swarm_client._drone_clients = {"1": drone_mock, "2": drone_mock, "3": drone_mock}
    calls = [mocker.call(), mocker.call(), mocker.call()]

    swarm_client.force_end_mission()

    drone_mock.force_end_mission.assert_has_calls(calls)


def test_return_to_base(app, mocker, swarm_client):
    drone_mock = mocker.Mock(SimulationDroneClient)
    swarm_client._drone_clients = {"1": drone_mock, "2": drone_mock, "3": drone_mock}
    calls = [mocker.call(), mocker.call(), mocker.call()]

    swarm_client.return_to_base()

    drone_mock.return_to_base.assert_has_calls(calls)


def test_identify(app, mocker, swarm_client):
    drone_mock = mocker.Mock(SimulationDroneClient)
    drone_mock.uri = '6666'
    swarm_client._drone_clients = {"1": drone_mock, "2": drone_mock, "3": drone_mock}
    calls = [mocker.call(), mocker.call(), mocker.call()]

    swarm_client.identify('6666')

    drone_mock.identify.assert_has_calls(calls)
