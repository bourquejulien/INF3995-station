from unittest import mock
import pytest
from src.classes.events.mission import Mission
from src.services.mission_service import MissionService
from src.exceptions.custom_exception import CustomException

from src.services.database_service import DatabaseService

ERROR = CustomException('test', 'test')


@pytest.fixture()
def mission_service():
    database_service_mock = mock.Mock(DatabaseService)
    config_mock = mock.Mock()
    mission_service = MissionService(config_mock, database_service_mock)
    yield mission_service


def test_start_mission_not_ongoing(app, mocker, mission_service):
    generate_mock = mocker.patch('src.services.mission_service.generate_mission')
    generate_mock.return_value = 'test'

    result = mission_service.start_mission(0)

    assert result == 'test'


def test_start_mission_ongoing(app, mocker, mission_service):
    mission_service._mission = 'test'

    try:
        mission_service.start_mission(0)
    except Exception as e:
        assert e.message == "Mission already started"


def test_end_mission_ongoing(app, mocker, mission_service):
    mission = Mission(True, 0, 0, 0, 0, 0)
    mission_service.flush = mocker.Mock(return_value=mission)

    mission_service.end_mission()

    mission_service._database_service.add.assert_called_once_with(mission)


def test_end_mission_not_ongoing(app, mocker, mission_service):
    mission_service.flush = mocker.Mock(return_value=None)

    mission_service.end_mission()

    mission_service._database_service.add.assert_not_called()


def test_flush(app, mocker, mission_service):
    flush_mock = mocker.Mock()
    mission_service._flush_callbacks = [flush_mock]

    mission_service.flush()

    flush_mock.assert_called_once()
    assert mission_service._mission == None


def test_get_last_missions(app, mocker, mission_service):
    mission_service.get_last_missions(0)

    mission_service._database_service.get_missions.assert_called_once_with(0)


def test_get_mission_by_id(app, mocker, mission_service):
    mission_service.get_mission_by_id('test')

    mission_service._database_service.get_mission.assert_called_once_with('test')


def test_add_flush_action(app, mocker, mission_service):
    mission_service._flush_callbacks = mocker.Mock()

    mission_service.add_flush_action('test')

    mission_service._flush_callbacks.append.assert_called_once_with('test')


def test_current_mission(app, mocker, mission_service):
    mission = Mission(True, 0, 0, 0, 0, 0)
    mission_service._mission = mission

    result = mission_service.current_mission

    assert result == mission
