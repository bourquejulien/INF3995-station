from flask import Blueprint
from flask import request
from flask.json import jsonify
from flask.views import MethodView
from src.services.command_service import CommandService
import sys

class WebController(MethodView):

    def __init__(self):
        self.commandService = CommandService()

    def post(self):
        request_data = request.get_json()
        response = {"status": "error"}

        if request_data["command"] == "init":
            response = self.commandService.init_mission(request_data)
        if request_data["command"] == "identify":
            response = self.commandService.identify(request_data)

        return jsonify(response)