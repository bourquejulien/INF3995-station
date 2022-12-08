import logging
import sys

from flask import Flask
from flask_cors import CORS
from src.controllers import (
    server_status_controller,
    discover_controller,
    mission_controller,
    action_controller,
    drone_info_controller,
    firmware_controller,
)
from src.services.command_service import CommandService
from dependency_injector.wiring import inject, Provide
from src.container import Container
from src.services.firmware_service.abstract_firmware_service import AbstractFirmwareService


def create_app():
    container = Container()

    app = Flask(__name__)
    CORS(app)
    app.container = container
    app.register_blueprint(server_status_controller.blueprint, url_prefix="/")
    app.register_blueprint(discover_controller.blueprint, url_prefix="/discovery")
    app.register_blueprint(mission_controller.blueprint, url_prefix="/mission")
    app.register_blueprint(action_controller.blueprint, url_prefix="/action")
    app.register_blueprint(drone_info_controller.blueprint, url_prefix="/drone-info")
    app.register_blueprint(firmware_controller.blueprint, url_prefix="/firmware")

    return app, container


@inject
def exit_app(
    command_service: CommandService = Provide[Container.command_service],
    firmware_service: AbstractFirmwareService = Provide[Container.firmware_service],
):
    logging.info("Exiting app...")
    firmware_service.close(sys.exc_info())
    command_service.disconnect()
