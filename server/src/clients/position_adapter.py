from collections import deque
from math import cos, sin, radians

from src.classes.distance import Distance
from src.classes.position import Position


def _convert_coordinate(position: Position):
    return Position(-position.y, position.x, position.z)


class _PositionHistory:
    _history: deque[(Position, Distance)]
    _average_size: int

    def __init__(self, average_size: int):
        self._history = deque()
        self._average_size = average_size

    def append(self, position: Position, distance: Distance):
        if not len(self._history) == 0 and len(self._history) >= self._average_size:
            self._history.pop()
        self._history.appendleft((position, distance))

    def clear(self):
        self._history.clear()

    def get_average(self):
        totalPosition = Position(0, 0, 0)
        totalDistance = Distance(0, 0, 0, 0)

        for position, distance in self._history:
            totalPosition = totalPosition + position
            totalDistance = totalDistance + distance

        return totalPosition * (1 / len(self._history)), totalDistance * (1 / len(self._history))

    def append_and_get(self, position, distance):
        self.append(position, distance)
        return self.get_average()


class PositionAdapter:
    _initial_position: Position
    _desired_position: Position
    _yaw: float
    _distance_trigger: float
    _position_history: _PositionHistory

    def __init__(self, distance_trigger: float, history_size: int):
        self._initial_position = Position(0, 0, 0)
        self._desired_position = Position(0, 0, 0)
        self._yaw = 0.0
        self._distance_trigger = distance_trigger
        self._position_history = _PositionHistory(history_size)

    def adapt(self, position: Position):
        position = _convert_coordinate(position)
        position = position + (self._initial_position * -1)

        x = position.x * cos(self._yaw) - position.y * sin(self._yaw)
        y = position.x * sin(self._yaw) + position.y * cos(self._yaw)

        return Position(
            x + self._desired_position.x, y + self._desired_position.y, position.z + self._desired_position.z
        )

    def set_position(self, current_position: Position, desired_position: Position, yaw_deg: float):
        self._yaw = radians(yaw_deg)
        self._desired_position = desired_position
        self._initial_position = _convert_coordinate(current_position)
        self._position_history.clear()

    def compute_distances(self, position: Position, distance: Distance):
        front = distance.front
        back = distance.back
        left = distance.left
        right = distance.right

        position, distance = self._position_history.append_and_get(position, distance)

        position = self.adapt(position)
        x, y = position.x, position.y

        position_distances = []

        if 0.01 < front < self._distance_trigger:
            position_distances.append(Position(x, y + front, 0))
        if 0.01 < back < self._distance_trigger:
            position_distances.append(Position(x, y - back, 0))
        if 0.01 < left < self._distance_trigger:
            position_distances.append(Position(x - left, y, 0))
        if 0.01 < right < self._distance_trigger:
            position_distances.append(Position(x + right, y, 0))

        return Position(x, y, position.z), position_distances
