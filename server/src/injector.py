from src.clients.phy_swarm_client import SwarmClient, PhySwarmClient
from src.clients.sim_swarm_client import SimSwarmClient
from src.services.command_service import CommandService
from src.services.persistent_service import PersistentService


class Injector:
    def __init__(self, is_simulation):
        self._mapping = {}
        self._isSimulation = is_simulation

    def _generate_clients(self):
        self._mapping[SwarmClient] = SimSwarmClient() if self._isSimulation else PhySwarmClient()

    def _generate_services(self):
        droneClient = self._mapping.get(SwarmClient)
        persistentService = PersistentService(droneClient)
        commandService = CommandService(droneClient, persistentService)
        self._mapping[PersistentService] = persistentService
        self._mapping[CommandService] = commandService

    def generate(self):
        self._generate_clients()
        self._generate_services()

    def get(self, service):
        return self._mapping.get(service)
