from flask import Blueprint, jsonify
from dependency_injector.wiring import inject, Provide
from src.container import Container
from src.exceptions.custom_exception import CustomException
from src.services.mission_service import MissionService

blueprint = Blueprint('mission', __name__)


@blueprint.route('/current_mission', methods=['get'])
@inject
def current_mission(mission_service: MissionService = Provide[Container.mission_service]):
    try:
        mission = mission_service.current_mission
        jsonify(mission.to_json())
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200


@blueprint.route('/start', methods=['post'])
@inject
def start(command_service=Provide[Container.command_service]):
    try:
        command_service.start_mission()
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200


@blueprint.route('/end', methods=['post'])
@inject
def end(command_service=Provide[Container.command_service]):
    try:
        command_service.end_mission()
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200


@blueprint.route('/force_end', methods=['post'])
@inject
def force_end(command_service=Provide[Container.command_service]):
    try:
        command_service.force_end_mission()
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200
