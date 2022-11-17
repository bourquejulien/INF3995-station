from dependency_injector.wiring import Provide, inject

from src.application import create_app, exit_app
from src.container import Container
import atexit

from src.services.command_service import CommandService
from src.services.database_service import DatabaseService
from src.services.firmware_service.abstract_firmware_service import AbstractFirmwareService
from src.services.logging_service import LoggingService
from src.services.mapping_service import MappingService
from src.services.mission_service import MissionService
from src.services.telemetrics_service import TelemetricsService


@inject
def main(app, command_service: CommandService = Provide[Container.command_service],
         mapping_service: MappingService = Provide[Container.mapping_service],
         logging_service: LoggingService = Provide[Container.logging_service],
         mission_service: MissionService = Provide[Container.mission_service],
         telemetrics_service: TelemetricsService = Provide[Container.telemetrics_service],
         firmware_service: AbstractFirmwareService = Provide[Container.firmware_service],
         database_service: DatabaseService = Provide[Container.database_service]):

    database_service.connect()
    command_service.connect(command_service.discover())
    app.run(host="0.0.0.0")


def exit_handler():
    exit_app()


if __name__ == "__main__":
    app, container = create_app()
    container.wire(modules=[".application", __name__], packages=[".controllers"], from_package="src")

    atexit.register(exit_handler)

    main(app)
