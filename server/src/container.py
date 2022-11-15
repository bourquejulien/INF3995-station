import os

from dependency_injector import containers, providers
from src.services.command_service import CommandService
from src.clients.simulation_swarm_client import SimulationSwarmClient
from src.clients.physical_swarm_client import PhysicalSwarmClient
from src.services.database_service import DatabaseService
from src.services.firmware_service import FirmwareService
from src.services.logging_service import LoggingService
from src.services.mapping_service import MappingService
from src.services.mission_service import MissionService
from src.services.telemetrics_service import TelemetricsService


class Container(containers.DeclarativeContainer):
    config = providers.Configuration(strict=True)
    config.from_yaml(f'{os.path.dirname(__file__)}/../config.yml', required=True)

    if config.get("is_simulation"):
        abstract_swarm_client = providers.Singleton(
            SimulationSwarmClient,
            config=config,
        )
    else:
        abstract_swarm_client = providers.Singleton(
            PhysicalSwarmClient,
            config=config,
        )

    database_service = providers.Singleton(
        DatabaseService,
        config=config,
    )

    mission_service = providers.Singleton(
        MissionService,
        config=config,
        database_service=database_service,
    )

    logging_service = providers.Singleton(
        LoggingService,
        swarm_client=abstract_swarm_client,
        mission_service=mission_service,
        database_service=database_service,
    )

    telemetrics_service = providers.Singleton(
        TelemetricsService,
        swarm_client=abstract_swarm_client,
        mission_service=mission_service,
        database_service=database_service,
        logging_service=logging_service,
    )

    mapping_service = providers.Singleton(
        MappingService,
        config=config,
        swarm_client=abstract_swarm_client,
        mission_service=mission_service,
        logging_service=logging_service,
    )

    command_service = providers.Singleton(
        CommandService,
        swarm_client=abstract_swarm_client,
        mission_service=mission_service,
        logging_service=logging_service,
    )

    firmware_service = providers.Singleton(
        FirmwareService,
        command_service=command_service
    )
