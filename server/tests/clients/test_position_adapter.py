import pytest
from math import radians
from src.classes.position import Position
from src.classes.distance import Distance
from src.clients.position_adapter import _convert_coordinate, \
        _PositionHistory, PositionAdapter


@pytest.fixture()
def position_history():
    yield _PositionHistory(0)


@pytest.fixture()
def position_adapter():
    yield PositionAdapter(0.0, 0)


def test_convert_coordinate(app, mocker):
    position = Position(1, 2, 3)

    result = _convert_coordinate(position)

    assert result.x == -2
    assert result.y == 1
    assert result.z == 3


def test_append(app, mocker, position_history):
    position = Position(1, 2, 3)

    position_history.append(position, 0)

    assert len(position_history._history) == 1


def test_clear(app, mocker, position_history):
    position_history._history = mocker.Mock()

    position_history.clear()

    position_history._history.clear.assert_called_once()


def test_get_average(app, mocker, position_history):
    position1 = Position(1, 2, 3)
    distance1 = Distance(1.0, 2.0, 3.0, 4.0)
    position2 = Position(3, 2, 1)
    distance2 = Distance(4.0, 3.0, 2.0, 1.0)
    position_history._history.appendleft((position1, distance1))
    position_history._history.appendleft((position2, distance2))

    result = position_history.get_average()

    assert result == (Position(2, 2, 2), Distance(2.5, 2.5, 2.5, 2.5))


def test_append_and_get(app, mocker, position_history):
    position = Position(1, 2, 3)
    distance = Distance(1.0, 2.0, 3.0, 4.0)
    position_history.append = mocker.Mock()
    position_history.get_average = mocker.Mock()

    position_history.append_and_get(position, distance)

    position_history.append.assert_called_once_with(position, distance)
    position_history.get_average.assert_called_once()


def test_adapt(app, mocker, position_adapter):
    position = Position(1, 2, 3)
    convert_coordinate_mock = mocker.patch('src.clients.position_adapter._convert_coordinate')
    convert_coordinate_mock.return_value = Position(-2, 1, 3)
    position_adapter._yaw = 0
    position_adapter._desired_position.x = 3
    position_adapter._desired_position.y = 3
    position_adapter._desired_position.z = 3

    result = position_adapter.adapt(position)

    assert result == Position(1, 4, 6)


def test_set_position(app, mocker, position_adapter):
    current_pos = Position(1, 2, 3)
    desired_pos = Position(2, 3, 4)
    yaw_deg = 5.0
    position_adapter._position_history = mocker.Mock()
    convert_coordinate_mock = mocker.patch('src.clients.position_adapter._convert_coordinate')
    convert_coordinate_mock.return_value = Position(-2, 1, 3)

    result = position_adapter.set_position(current_pos, desired_pos, yaw_deg)

    assert position_adapter._yaw == radians(yaw_deg)
    assert position_adapter._desired_position == desired_pos
    assert position_adapter._initial_position == Position(-2, 1, 3)
    position_adapter._position_history.clear.assert_called_once()


def test_compute_distances(app, mocker, position_adapter):
    position = Position(1, 2, 3)
    distance = Distance(1.0, 2.0, 3.0, 4.0)

    result = position_adapter.compute_distances(position, distance)

    assert result == (Position(-2, 1, 3), [])
