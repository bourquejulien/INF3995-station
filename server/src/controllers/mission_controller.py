from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from src.container import Container
from src.exceptions.custom_exception import CustomException
from src.services.mission_service import MissionService
from src.services.logging_service import LoggingService
from src.services.telemetrics_service import TelemetricsService

blueprint = Blueprint('mission', __name__)


@blueprint.route('/', methods=['get'])
@inject
def get_missions(mission_service: MissionService = Provide[Container.mission_service]):
    try:
        mission_id = request.args.get('mission_id', type=str)
        missions = []
        if mission_id is not None:
            missions.append(mission_service.get_mission_by_id(mission_id))
        else:
            start_timestamp = request.args.get('start_timestamp', type=int)
            end_timestamp = request.args.get('end_timestamp', type=int)
            missions.append(mission_service.get_missions_range(start_timestamp, end_timestamp))
        jsonify(missions.to_json())
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200


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
        mission = command_service.start_mission()
    except CustomException as e:
        return '"error": "{}: {}"'.format(e.name, e.message), 500
    return mission.to_json(), 200


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


@blueprint.route('/logs', methods=['get'])
@inject
def get_logs(logging_service: LoggingService = Provide[Container.logging_service]):
    try:
        mission_id = request.args.get('mission_id', type=str)
        logs_list = logging_service.get_history(mission_id)
        return jsonify(logs_list)
    except CustomException as e:
        return f"{e.name}: {e.message}", 500


@blueprint.route('/metrics', methods=['get'])
@inject
def get_metrics(telemetrics_service: TelemetricsService = Provide[Container.telemetrics_service]):
    try:
        mission_id = request.args.get('mission_id', type=str)
        metrics_list = telemetrics_service.get_history(mission_id)
        return jsonify(metrics_list)
    except CustomException as e:
        return f"{e.name}: {e.message}", 500
