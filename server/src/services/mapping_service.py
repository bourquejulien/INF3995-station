import math

from dependency_injector.providers import Configuration

from src.classes.distance import Distance
from src.classes.position import Position
from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.services.logging_service import LoggingService
from src.services.mission_service import MissionService


def _compute_position(position: Position, distance: Distance, trigger: float):
    points = []

    if distance.front < trigger:
        points.append(Position(position.x, position.y + distance.front, position.z))
    if distance.back < trigger:
        points.append(Position(position.x, position.y - distance.back, position.z))
    if distance.left < trigger:
        points.append(Position(position.x - distance.left, position.y, position.z))
    if distance.right < trigger:
        points.append(Position(position.x + distance.right, position.y, position.z))

    return points


def _remove_duplicate(points: list[Position], new_points: list[Position], duplicate_distance: float):
    distance = lambda a, b: math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)

    for point in points:
        duplicates = []
        for i, new_point in enumerate(new_points):
            if (distance(point, new_point)) < duplicate_distance:
                duplicates.append(i)
        for x in reversed(duplicates):
            new_points.pop(x)


class MappingService:
    _config: Configuration
    _logging_service: LoggingService
    _maps: dict[str, list[Position]]

    def __init__(self, config: Configuration, swarm_client: AbstractSwarmClient, mission_service: MissionService,
                 logging_service: LoggingService):
        self._maps = {}
        self._logging_service = logging_service
        self._config = config
        swarm_client.add_callback("mapping", self._add)
        mission_service.add_flush_action(self.flush)

    def _add(self, uri, position: Position, distance: Distance):
        self._logging_service.log(f"Received distance: {distance}, uri: {uri}")
        new_points = _compute_position(position, distance, float(self._config["mapping"]["trigger_distance"]))
        if uri in self._maps:
            points = self._maps.get(uri)
        else:
            points = []
            self._maps[uri] = points

        _remove_duplicate(points, new_points, float(self._config["mapping"]["duplicate_distance"]))
        points.extend(new_points)

    def get_map(self, uri):
        return self._maps.get(uri)

    def flush(self):
        self._maps.clear()
