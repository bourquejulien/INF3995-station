from unittest import mock
import pytest
from src.clients.abstract_swarm_client import AbstractSwarmClient

from src.services.mission_service import MissionService
from src.services.logging_service import LoggingService
from src.services.database_service import DatabaseService
from src.classes.events.log import Log
from src.classes.events.mission import Mission


@pytest.fixture()
def log_service():
    client_mock = mock.Mock(AbstractSwarmClient)
    mission_service_mock = mock.Mock(AbstractSwarmClient)
    mission_service_mock = mock.Mock(MissionService)
    db_service_mock = mock.Mock(DatabaseService)
    log_service = LoggingService(client_mock, mission_service_mock, db_service_mock)
    yield log_service


def test_add(app, log_service):
    log = Log("", 0, "test", "", "", "")

    log_service._add(log)

    assert log_service._logs.pop() == log


def test_add_with_current_mission(app, log_service):
    log = Log("", 0, "test", "", "", "")
    mission = Mission(True, 0, 0, 0, 0, 0)
    log_service._mission_service.current_mission = mission

    log_service._add(log)
    result = log_service._logs.pop()
    assert result == log


def test_log(app, mocker, log_service):
    log_service._add = mocker.Mock()

    log_service.log("test_id", "test_origin")

    log_service._add.assert_called_once()


def test_get_since(app, mocker, log_service):
    log1 = Log("", 0, "test", "", "", "")
    log2 = Log("", 1, "test", "", "", "")

    log_service._logs.append(log1)
    log_service._logs.append(log2)

    result = log_service.get_since("test", 0)

    assert result == [log2]


def test_get_history(app, mocker, log_service):
    log_service._database_service.get_logs = mocker.Mock()

    log_service.get_history("test")

    log_service._database_service.get_logs.assert_called_once_with("test")


def test_flush(app, mocker, log_service):
    mission = Mission(True, 0, 0, 0, 0, 0)
    log_service._mission_service.current_mission = mission
    log_service._database_service.add_many = mocker.Mock()

    log_service.flush()

    log_service._database_service.add_many.assert_called_once_with([])
