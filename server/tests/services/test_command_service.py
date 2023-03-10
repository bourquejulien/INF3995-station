from unittest import mock
import pytest
from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.services.command_service import CommandService
from src.exceptions.custom_exception import CustomException

from src.services.logging_service import LoggingService

ERROR = CustomException("test", "test")


@pytest.fixture()
def command_service():
    client_mock = mock.Mock(AbstractSwarmClient)
    client_mock.uris = []
    mission_service_mock = mock.Mock(AbstractSwarmClient)
    logging_service_mock = mock.Mock(LoggingService)
    mission_service_mock.current_mission = None
    command_service = CommandService(client_mock, mission_service_mock, logging_service_mock)
    yield command_service


def test_start_mission(app, command_service):
    command_service._config = {"is_simulation": True}
    command_service.start_mission()

    command_service._swarm_client.start_mission.assert_called_once()


def test_start_mission_error(app, command_service):
    command_service._swarm_client.start_mission.side_effect = ERROR

    try:
        command_service.start_mission()
    except CustomException as e:
        error = e
    assert error.message == "test"


def test_end_mission(app, command_service):
    command_service.end_mission()
    command_service._swarm_client.end_mission.assert_called_once()


def test_end_mission_error(app, command_service):
    command_service._swarm_client.end_mission.side_effect = ERROR

    try:
        command_service.end_mission()
    except CustomException as e:
        error = e
    assert error.message == "test"


def test_force_end_mission(app, command_service):
    command_service.force_end_mission()
    command_service._swarm_client.force_end_mission.assert_called_once()


def test_force_end_mission_error(app, command_service):
    command_service._swarm_client.force_end_mission.side_effect = ERROR

    try:
        command_service.force_end_mission()
    except CustomException as e:
        error = e
    assert error.message == "test"


def test_return_to_base(app, command_service):
    command_service.return_to_base()
    command_service._swarm_client.return_to_base.assert_called_once()


def test_return_to_base_error(app, command_service):
    command_service._swarm_client.return_to_base.side_effect = ERROR

    try:
        command_service.return_to_base()
    except CustomException as e:
        error = e
    assert error.message == "test"


def test_identify(app, command_service):
    uris = ["test"]

    command_service.identify(uris)

    command_service._swarm_client.identify.assert_called_once_with(uris)


def test_identify_error(app, command_service):
    command_service._swarm_client.identify.side_effect = ERROR
    uris = ["test"]

    try:
        command_service.identify(uris)
    except CustomException as e:
        error = e
    assert error.message == "test"


def test_toggle_synchronization(app, mocker, command_service):
    command_service.toggle_synchronization()

    command_service._swarm_client.toggle_drone_synchronisation.assert_called_once()


def test_toggle_synchronization_error(app, command_service):
    command_service._swarm_client.toggle_drone_synchronisation.side_effect = ERROR

    try:
        command_service.toggle_synchronization()
    except CustomException as e:
        error = e
    assert error.message == "test"


def test_set_initial_positions(app, mocker, command_service):
    command_service.set_initial_positions([])

    command_service._swarm_client.set_initial_positions.assert_called_once()


def test_set_initial_positions_error(app, command_service):
    command_service._swarm_client.set_initial_positions.side_effect = ERROR

    try:
        command_service.set_initial_positions([])
    except CustomException as e:
        error = e
    assert error.message == "test"


def test_connect(app, command_service):
    uris = ["test"]

    command_service.connect(uris)

    command_service._swarm_client.connect.assert_called_once_with(uris)


def test_connect_error(app, command_service):
    command_service._swarm_client.connect.side_effect = ERROR
    uris = ["test"]

    try:
        command_service.connect(uris)
    except CustomException as e:
        error = e
    assert error.message == "test"


def test_disconnect(app, command_service):
    command_service._swarm_client.disconnect.return_value = ""

    command_service.disconnect()

    command_service._swarm_client.disconnect.assert_called_once()


def test_disconnect_error(app, command_service):
    command_service._swarm_client.disconnect.side_effect = ERROR

    try:
        command_service.disconnect()
    except CustomException as e:
        error = e
    assert error.message == "test"


def test_discover(app, command_service):
    command_service._swarm_client.discover.return_value = ""

    command_service.discover()

    command_service._swarm_client.discover.assert_called_once()


def test_discover_error(app, command_service):
    command_service._swarm_client.discover.side_effect = ERROR

    try:
        command_service.discover()
    except CustomException as e:
        error = e
    assert error.message == "test"
