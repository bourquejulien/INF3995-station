from unittest import mock
import pytest
from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.classes.events.metric import Metric
from src.classes.events.mission import Mission
from src.classes.position import Position
from src.services.telemetrics_service import TelemetricsService
from src.services.database_service import DatabaseService
from src.services.logging_service import LoggingService
from src.services.mission_service import MissionService


@pytest.fixture()
def telemetrics_service(mocker):
    client_mock = mock.Mock(AbstractSwarmClient)
    mission_service_mock = mock.Mock(MissionService)
    db_service_mock = mock.Mock(DatabaseService)
    logging_service_mock = mock.Mock(LoggingService)
    telemetrics_service = TelemetricsService(client_mock, mission_service_mock, db_service_mock, logging_service_mock)
    yield telemetrics_service


def test_add(app, mocker, telemetrics_service):
    metric = Metric(0, Position(0, 0, 0), "", "", "", "test", 0)
    mission = Mission(True, "", 0, 0, 0, 0)
    telemetrics_service._mission_service.current_mission = mission

    telemetrics_service._add(metric)

    telemetrics_service._logging_service.log.assert_called_once()
    assert telemetrics_service._metrics[0] == metric


def test_get_since(app, mocker, telemetrics_service):
    metric1 = Metric(Position(0, 0, 0), 0, "", "", "", "test", 0)
    metric2 = Metric(Position(0, 0, 0), 1, "", "", "", "test", 0)
    telemetrics_service._metrics = [metric2, metric1]

    result = telemetrics_service.get_since(0)

    assert result == [metric2]


def test_get_history(app, mocker, telemetrics_service):
    telemetrics_service._database_service.get_metrics = mocker.Mock()

    result = telemetrics_service.get_history("test")

    telemetrics_service._database_service.get_metrics.assert_called_once_with("test")


def test_flush(app, mocker, telemetrics_service):
    metric1 = Metric(Position(0, 0, 0), 0, "", "", "", "test", 0)
    metric2 = Metric(Position(0, 0, 0), 1, "", "", "", "test", 0)
    telemetrics_service._metrics = [metric2, metric1]
    mission = Mission(True, "", 0, 0, 0, 0)
    telemetrics_service._mission_service.current_mission = mission

    telemetrics_service.flush()

    assert telemetrics_service._metrics == []
    assert telemetrics_service._latest == {}


def test_latest(app, mocker, telemetrics_service):
    telemetrics_service._latest = "test"

    result = telemetrics_service.latest

    assert result == "test"
