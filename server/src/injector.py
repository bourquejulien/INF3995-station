from src.clients.drone_client import DroneClient
from src.clients.simulation_client import SimulationClient
from src.clients.swarm_client import SwarmClient
from src.services.command_service import CommandService
from src.services.persistent_service import PersistentService


class Injector:
    def __init__(self, is_simulation):
        self._mapping = {}
        self._isSimulation = is_simulation

    def _generate_clients(self):
        self._mapping[DroneClient] = SimulationClient() if self._isSimulation else SwarmClient()

    def _generate_services(self):
        droneClient = self._mapping[DroneClient]
        persistentService = PersistentService(droneClient)
        commandService = CommandService(droneClient, persistentService)
        self._mapping[PersistentService] = persistentService
        self._mapping[CommandService] = commandService

    def generate(self):
        self._generate_clients()
        self._generate_services()

    def get(self, service):
        return self._mapping.get(service)
