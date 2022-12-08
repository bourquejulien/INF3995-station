from dependency_injector.providers import Configuration
from src.classes.events.mapInfo import MapInfo, generate_mapInfo

from src.classes.position import Position
from src.classes.events.mapDatabase import generate_mapDatabase
from src.classes.vec2 import Vec2
from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.services.logging_service import LoggingService
from src.services.mission_service import MissionService
from src.services.database_service import DatabaseService


class MappingService:
    _config: Configuration
    _logging_service: LoggingService
    _mission_service: MissionService
    _database_service: DatabaseService
    _maps: dict[str, list[MapInfo]]  # For live map on client
    _latest: dict[str, MapInfo]

    def __init__(
        self,
        config: Configuration,
        swarm_client: AbstractSwarmClient,
        mission_service: MissionService,
        logging_service: LoggingService,
        database_service: DatabaseService,
    ):
        self._maps = {}
        self._latest = {}
        self._logging_service = logging_service
        self._config = config
        self._mission_service = mission_service
        self._database_service = database_service
        swarm_client.add_callback("mapping", self._add)
        mission_service.add_flush_action(self.flush)

    def _add(self, uri, position: Position, distances: list[Position]):
        log = f"Received distance: {distances}, Position: {position}, Uri: {uri}"
        self._logging_service.log(log)
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
        return self._maps.copy()

    def _convert_database_map(self):
        position_obstacle = []
        for drone in self._maps:
            for map_info in self._maps[drone]:
                for position in map_info.distance:
                    newPoint = Vec2(position.x, position.y)
                    position_obstacle.append(newPoint)
        map_database = generate_mapDatabase(position_obstacle, self._mission_service.current_mission.id)
        return map_database

    def flush(self):
        if self._mission_service.current_mission is not None:
            map_database = self._convert_database_map()
            self._database_service.add(map_database)

        self._maps.clear()
        self._latest.clear()
