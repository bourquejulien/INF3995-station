import math

from dependency_injector.providers import Configuration, Container
from dependency_injector.wiring import Provide, inject

from src.classes.distance import Distance
from src.classes.position import Position
from src.clients.abstract_swarm_client import AbstractSwarmClient


@inject
def _compute_position(position: Position, distance: Distance, config: Configuration = Provide[Container.config]):
    trigger = float(config["mapping"]["distance_trigger"])
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


@inject
def _remove_duplicate(points: list[Position], new_points: list[Position],
                      config: Configuration = Provide[Container.config]):
    duplicate_distance = float(config["mapping"]["duplicate_distance"])

    distance = lambda a, b: math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2 + (a.z - b.z) ** 2)

    for point in points:
        duplicates = []
        for i, new_point in enumerate(new_points):
            if (distance(point, new_point)) < duplicate_distance:
                duplicates.append(i)
        for x in duplicates:
            new_points.pop(x)


class MappingService:
    _maps: dict[str, list[Position]]

    def __init__(self, swarm_client: AbstractSwarmClient):
        self._maps = {}
        swarm_client.add_callback("mapping", self._add)

    def _add(self, uri, position: Position, distance: Distance):
        new_points = _compute_position(position, distance)

        if uri in self._maps:
            points = self._maps.get(uri)
        else:
            points = []
            self._maps[uri] = points

        _remove_duplicate(points, new_points)
        points.extend(new_points)

    def get_map(self, uri):
        return self._maps.get(uri)

    def flush(self):
        self._maps.clear()
