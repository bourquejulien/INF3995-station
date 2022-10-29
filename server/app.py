from dependency_injector.wiring import Provide, inject

from src.application import create_app, exit_app
from src.container import Container
import atexit

from src.services.command_service import CommandService


@inject
def main(app, command_service: CommandService = Provide[Container.command_service]):
    command_service.connect(command_service.discover())
    app.run(host="0.0.0.0")


def exit_handler():
    exit_app()


if __name__ == "__main__":
    app, container = create_app()
    container.wire(modules=[".application", __name__], packages=[".controllers", ".services"], from_package="src")

    atexit.register(exit_handler)

    main(app)
