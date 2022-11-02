import os

from dependency_injector import containers, providers
from src.services.command_service import CommandService
from src.clients.simulation_swarm_client import SimulationSwarmClient
from src.clients.physical_swarm_client import PhysicalSwarmClient
from src.services.database_service import DatabaseService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(strict=True)
    config.from_yaml(f'{os.path.dirname(__file__)}/../config.yml', required=True)

    if config.get("is_simulation"):
        abstract_swarm_client = providers.Singleton(
            SimulationSwarmClient,
            config=config
        )
    else:
        abstract_swarm_client = providers.Singleton(
            PhysicalSwarmClient,
        )

    command_service = providers.Singleton(
        CommandService,
        swarm_client=abstract_swarm_client,
        config=config,
    )

    database_service = providers.Singleton(
        DatabaseService,
        config=config,
    )
