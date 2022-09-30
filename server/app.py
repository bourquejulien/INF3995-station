from os import environ as env
from flask import Flask, jsonify
from flask_cors import CORS

from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.controllers import discover_controller, mission_controller, action_controller
from src.injector import Injector
from src.services.command_service import CommandService
from src.services.startup_service import StartupService

app = Flask(__name__)
is_simulation = env.get("IS_SIMULATION").lower() == "true" if env.get("IS_SIMULATION") is not None else True
injector = Injector(is_simulation)


@app.route('/health')
def health():
    return 'healthy'


@app.route('/is_simulation', methods=['GET'])
def run_mode():
    return jsonify(is_simulation)


def setup():
    CORS(app)
    injector.generate()
    discover_controller.startupService = injector.get(StartupService)
    action_controller.command_service = injector.get(CommandService)
    mission_controller.swarm_client = injector.get(AbstractSwarmClient)
    app.register_blueprint(discover_controller.blueprint, url_prefix="/discovery")
    app.register_blueprint(mission_controller.blueprint, url_prefix="/mission")
    app.register_blueprint(action_controller.blueprint, url_prefix="/action")


def main():
    setup()
    startup_service = injector.get(StartupService)
    startup_service.start()

    if len(startup_service.drones_ids) == 0:
        print("No drone detected")
        return 1

    app.run(host="0.0.0.0")
    startup_service.disconnect()


if __name__ == '__main__':
    main()
