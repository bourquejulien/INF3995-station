from src.clients.physical_swarm_client import AbstractSwarmClient, PhysicalSwarmClient
from src.clients.simulation_swarm_client import SimulationSwarmClient
from src.services.command_service import CommandService
from src.services.startup_service import StartupService


class Injector:
    def __init__(self, is_simulation):
        self._mapping = {}
        self._isSimulation = is_simulation

    def _generate_clients(self):
        self._mapping[AbstractSwarmClient] = SimulationSwarmClient() if self._isSimulation else PhysicalSwarmClient()

    def _generate_services(self):
        droneClient = self._mapping.get(AbstractSwarmClient)
        persistentService = StartupService(droneClient)
        commandService = CommandService(droneClient, persistentService)
        self._mapping[StartupService] = persistentService
        self._mapping[CommandService] = commandService

    def generate(self):
        self._generate_clients()
        self._generate_services()

    def get(self, service):
        return self._mapping.get(service)
