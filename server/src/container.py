import sys

from dependency_injector import containers, providers
from src.services.command_service import CommandService
from src.clients.simulation_swarm_client import SimulationSwarmClient
from src.clients.physical_swarm_client import PhysicalSwarmClient


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(strict=True)
    config.from_yaml('config.yml', required=True)

    if config.get("is_simulation"):
        abstract_swarm_client = providers.Factory(
            SimulationSwarmClient,
            config=config
        )
    else:
        abstract_swarm_client = providers.Factory(
            PhysicalSwarmClient,
        )

    command_service = providers.Factory(
        CommandService,
        swarm_client=abstract_swarm_client,
    )
