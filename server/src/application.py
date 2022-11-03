from flask import Flask
from flask_cors import CORS
from src.controllers import server_status_controller, discover_controller, \
    mission_controller, action_controller, drone_info_controller
from src.services.command_service import CommandService
from dependency_injector.wiring import inject, Provide
from src.container import Container


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

    return app, container


@inject
def exit_app(command_service: CommandService = Provide[Container.command_service]):
    print("Exiting app...")
    command_service.disconnect()
