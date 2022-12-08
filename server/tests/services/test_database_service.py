from unittest import mock
import pytest
import mongomock
from src.classes.events.log import Log
from dependency_injector.providers import Configuration
from src.services.database_service import DatabaseService, MAPPING


@pytest.fixture()
def db_service():
    configuration_mock = mock.Mock(Configuration)
    db_service = DatabaseService(configuration_mock)
    db_service._collections = mongomock.MongoClient().db.collection
    yield db_service


def test_connect(app, mocker, db_service):
    db_service._config = {"database": {"connection_string": "mock_connection", "name": ""}}
    mocker.patch('src.services.database_service.MongoClient')

    db_service.connect()


def test_add(app, mocker, db_service):
    event = mocker.Mock()
    db_service.add_many = mocker.Mock()

    db_service.add(event)

    db_service.add_many.assert_called_once_with([event])


def test_add_many(app, mocker, db_service):
    data = [Log("", 0, "test", "", "", "")]
    db_service._add_many = mocker.Mock()

    db_service.add_many(data)

    db_service._add_many.assert_called_once_with(
            data, MAPPING[data[0].__class__])


def test_get_logs(app, mocker, db_service):
    log1 = {'mission_id': 'test', 'timestamp_ms': 0,
            'message': '', 'level': '', 'origin': ''}
    log2 = {'mission_id': 'patate', 'timestamp_ms': 0,
            'message': '', 'level': '', 'origin': ''}
    db_service._collections['log'].insert_one(log1)
    db_service._collections['log'].insert_one(log2)

    result = db_service.get_logs('test')

    assert len(result) == 1


def test_get_metrics(app, mocker, db_service):
    metric1 = {'mission_id': 'test', 'timestamp_ms': 0,
               'position': '', 'status': '', 'uri': '', 'battery_level': 0.0}
    metric2 = {'mission_id': 'patate', 'timestamp_ms': 0,
               'position': '', 'status': '', 'uri': '', 'battery_level': 0.0}
    db_service._collections['metric'].insert_one(metric1)
    db_service._collections['metric'].insert_one(metric2)

    result = db_service.get_metrics('test')

    assert len(result) == 1


def test_get_mission(app, mocker, db_service):
    mission1 = {'drone_count': 1, 'end_time_ms': 1, '_id': '1',
                'is_simulation': True, 'start_time_ms': 1, 'total_distance': 1}
    mission2 = {'drone_count': 2, 'end_time_ms': 2, '_id': '2',
                'is_simulation': True, 'start_time_ms': 2, 'total_distance': 2}
    db_service._collections['mission'].insert_one(mission1)
    db_service._collections['mission'].insert_one(mission2)

    result = db_service.get_mission("1")

    result.pop("id")
    mission1.pop("_id")
    assert result == mission1


def test_get_missions(app, mocker, db_service):
    mission1 = {'drone_count': 1, 'end_time_ms': 1, '_id': '1',
                'is_simulation': True, 'start_time_ms': 1, 'total_distance': 1}
    mission2 = {'drone_count': 2, 'end_time_ms': 2, '_id': '2',
                'is_simulation': True, 'start_time_ms': 2, 'total_distance': 2}
    mission3 = {'drone_count': 3, 'end_time_ms': 3, '_id': '3',
                'is_simulation': True, 'start_time_ms': 3, 'total_distance': 3}
    db_service._collections['mission'].insert_one(mission1)
    db_service._collections['mission'].insert_one(mission2)
    db_service._collections['mission'].insert_one(mission3)

    result = db_service.get_missions(2)

    assert len(result) == 2


def test_add_many_private(app, mocker, db_service):
    log = Log("", 0, "test", "", "", "")
    elem = [log, log]
    db_service._collections = {}
    db_service._collections['test'] = mocker.Mock()

    result = db_service._add_many(elem, 'test')

    db_service._collections['test'].insert_many.assert_called_once()
