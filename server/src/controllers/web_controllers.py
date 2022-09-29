from flask import request
from flask.json import jsonify
from flask.views import MethodView

from src.injector import Injector
from src.services.command_service import CommandService

injector: Injector


class MissionController():

    def __init__(self):
        self.commandService: CommandService = injector.get(CommandService)

    def post(self):
        request_data = request.get_json()
        response = {"status": "error"}

        if request_data["command"] == "start":
            response = self.commandService.start_mission(request_data)
        if request_data["command"] == "end":
            response = self.commandService.end_mission(request_data)

        return jsonify(response)


class ActionController(MethodView):

    def __init__(self):
        self.commandService = injector.get(CommandService)

    def post(self):
        request_data = request.get_json()
        response = {"status": "error"}

        # TODO Handle drone actions

        return jsonify(response)
