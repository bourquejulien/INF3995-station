import json
from sched import scheduler

from src.clients.drone_clients.simulation_drone_client import SimulationDroneClient
from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.classes.position import Position


class SimulationSwarmClient(AbstractSwarmClient):
    def __init__(self, config):
        super().__init__()
        self._drone_clients = []
        self.config = config

    def start_mission(self):
        # TODO Ajouter un fonction periodique pour aller checher les position
        # scheduler.enter(interval, 1, periodic, (scheduler, interval, action, actionargs))
        # action(*actionargs)
        for drone in self._drone_clients:
            drone.start_mission()


    def end_mission(self):
        # TODO Arrêter la fonction periodique
        for drone in self._drone_clients:
            drone.end_mission()

    def force_end_mission(self):
        # TODO vérifier
        for drone in self._drone_clients:
            drone.force_end_mission()

    def identify(self, uris):
        for drone in self._drone_clients:
            if drone.uri in uris:
                drone.identify()

    def connect(self, uris):
        for uri in uris:
            client = SimulationDroneClient(self.config['argos']['hostname'], uri)
            client.connect()
            self._drone_clients.append(client)

    def disconnect(self):
        for drone in self._drone_clients:
            drone.disconnect()

    def discover(self):
        return [str(self.config['argos']['port']), str(self.config['argos']['port'] + 1)]

    def get_position(self):
        # TODO Format using Position dataclass
        drone_dict = {"positions": []}
        for drone in self._drone_clients:
            drone_position = drone.get_position()
            # pos_dict = {}
            # pos_dict["uri"] = drone.uri
            # pos_dict["posX"] = drone_position.posX
            # pos_dict["posY"] = drone_position.posY
            # pos_dict["posZ"] = drone_position.posZ
            # drone_dict['positions'].append(pos_dict)
            pos = Position(drone_position.posX, drone_position.posY, drone_position.posZ)
            drone_dict['positions'].append(pos)
        json_list = json.dumps(drone_dict)
        return json_list
