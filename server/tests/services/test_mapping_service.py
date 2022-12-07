from unittest import mock
import pytest
from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.classes.position import Position
from src.services.mapping_service import MappingService
from src.services.logging_service import LoggingService
from src.services.mission_service import MissionService


@pytest.fixture()
def mapping_service(mocker):
    config_mock = {'is_simulation': True}
    client_mock = mock.Mock(AbstractSwarmClient)
    mission_service_mock = mock.Mock(MissionService)
    logging_service_mock = mock.Mock(LoggingService)
    mapping_service = MappingService(config_mock,
                                     client_mock,
                                     mission_service_mock,
                                     logging_service_mock)
    yield mapping_service


def test_add(app, mocker, mapping_service):
    mapping_service._add('test_uri', Position(0, 0, 0), [])

    mapping_service._logging_service.log.assert_called_once()


def test_get_latest(app, mocker, mapping_service):
    mapping_service._latest = 'test'

    result = mapping_service.get_latest()

    assert result == 'test'


def test_get_map(app, mocker, mapping_service):
    mapping_service._maps = ['test']

    result = mapping_service.get_map()

    assert result == ['test']


def test_flush(app, mocker, mapping_service):
    mapping_service._maps = ['test']

    mapping_service.flush()

    assert mapping_service._maps == []
