import math

from dependency_injector.providers import Configuration
from src.classes.events.mapInfo import MapInfo, generate_mapInfo

from src.classes.distance import Distance
from src.classes.position import Position
from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.services.logging_service import LoggingService
from src.services.mission_service import MissionService


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
    _maps: dict[str, list[MapInfo]] # For live map on client
    _latest: dict[str, MapInfo]
    _is_simulation: bool

    def __init__(self, config: Configuration, swarm_client: AbstractSwarmClient, mission_service: MissionService,
                 logging_service: LoggingService):
        self._maps = {}
        self._latest = {}
        self._logging_service = logging_service
        self._config = config
        self._is_simulation = self._config["is_simulation"]
        swarm_client.add_callback("mapping", self._add)
        mission_service.add_flush_action(self.flush)

    def _add(self, uri, position: Position, distances):
        self._logging_service.log(f"Received distance: {distances}, Position: {position}, Uri: {uri}")
        new_map_info = generate_mapInfo(uri, position, distances)
        
        if uri in self._maps:
            self._maps[uri].append(new_map_info)
        else:
            self._maps[uri] = []
            self._maps[uri].append(new_map_info) 

        self._latest[uri] = new_map_info

    def get_latest(self):
        return self._latest

    def get_map(self):
        return self._maps

    def flush(self):
        self._maps.clear()
