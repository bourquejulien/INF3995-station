from os import environ as env
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

import src.controllers.web_controllers
from src.controllers import discover_controller
from src.controllers.web_controllers import ActionController, MissionController
from src.injector import Injector
from src.services.startup_service import StartupService

app = Flask(__name__)
is_simulation = env.get("IS_SIMULATION") if env.get("IS_SIMULATION") is not None else True
injector = Injector(is_simulation)


@app.route('/health')
def health():
    return 'healthy'


def setup():
    CORS(app)
    api = Api(app)
    injector.generate()
    src.controllers.web_controllers.injector = injector
    src.controllers.discover_controller.startupService = injector.get(StartupService)
    app.register_blueprint(discover_controller.blueprint, url_prefix="/discovery")
    api.add_resource(MissionController, "/mission")
    api.add_resource(ActionController, "/end")


def main():
    setup()
    startup_service = injector.get(StartupService)
    startup_service.start()

    if len(startup_service.drones_ids) == 0:
        print("No drone detected")
        return 1

    app.run(host="0.0.0.0")


if __name__ == '__main__':
    main()
