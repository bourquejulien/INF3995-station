import pytest
from src.clients.drone_syncer import DroneSyncer


@pytest.fixture()
def drone_syncer():
    yield DroneSyncer(['6666'])


def test_wait_with_set_event(app, mocker, drone_syncer):
    drone_syncer._event = mocker.Mock()
    drone_syncer._event.is_set.return_value = True

    drone_syncer.wait(0)

    drone_syncer._event.is_set.assert_called_once()
    drone_syncer._event.clear.assert_called_once()
    assert drone_syncer._blocked_uris == ['6666']


def test_wait_without_set_event(app, mocker, drone_syncer):
    drone_syncer._event = mocker.Mock()
    drone_syncer._event.is_set.return_value = False

    drone_syncer.wait(0)

    drone_syncer._event.is_set.assert_called_once()
    drone_syncer._event.clear.assert_not_called()
    assert drone_syncer._blocked_uris == []


def test_return_with_set_event(app, mocker, drone_syncer):
    drone_syncer._event = mocker.Mock()
    drone_syncer._event.is_set.return_value = True
    drone_syncer._blocked_uris = ['6666']

    drone_syncer.release('6666')

    assert not drone_syncer._blocked_uris == []


def test_return_without_set_event(app, mocker, drone_syncer):
    drone_syncer._event = mocker.Mock()
    drone_syncer._event.is_set.return_value = False
    drone_syncer._blocked_uris = ['6666']

    drone_syncer.release('6666')

    assert drone_syncer._blocked_uris == []


def test_remove_uri(app, mocker, drone_syncer):
    drone_syncer.release = mocker.Mock()

    drone_syncer.remove_uri('6666')

    assert drone_syncer._uris == []
    drone_syncer.release.assert_called_once_with('6666')


def test_close(app, mocker, drone_syncer):
    drone_syncer._blocked_uris = ['6666']
    drone_syncer._event = mocker.Mock()

    drone_syncer.close()

    assert drone_syncer._uris == []
    assert drone_syncer._blocked_uris == []
    drone_syncer._event.set.assert_called_once()
