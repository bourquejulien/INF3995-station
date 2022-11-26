import logging

from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from src.container import Container
from src.exceptions.custom_exception import CustomException
from src.services.mission_service import MissionService
from src.services.logging_service import LoggingService
from src.services.telemetrics_service import TelemetricsService

logger = logging.getLogger(__file__)
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
            missions_number = request.args.get('missions_number', type=int)
            missions = mission_service.get_last_missions(missions_number)
    except CustomException as e:
        logger.warning(e, exc_info=True)
        return "{}: {}".format(e.name, e.message), 500
    return jsonify(missions), 200


@blueprint.route('/current_mission', methods=['get'])
@inject
def current_mission(mission_service: MissionService = Provide[Container.mission_service]):
    try:
        mission = mission_service.current_mission
        if mission is not None:
            return jsonify(mission)
        return jsonify({})
    except CustomException as e:
        logger.warning(e, exc_info=True)
        return "{}: {}".format(e.name, e.message), 500


@blueprint.route('/start', methods=['post'])
@inject
def start(command_service=Provide[Container.command_service]):
    try:
        mission = command_service.start_mission()
    except CustomException as e:
        logger.warning(e, exc_info=True)
        return '"error": "{}: {}"'.format(e.name, e.message), 500
    return jsonify(mission), 200


@blueprint.route('/end', methods=['post'])
@inject
def end(command_service=Provide[Container.command_service]):
    try:
        command_service.end_mission()
    except CustomException as e:
        logger.warning(e, exc_info=True)
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200


@blueprint.route('/force_end', methods=['post'])
@inject
def force_end(command_service=Provide[Container.command_service]):
    try:
        command_service.force_end_mission()
    except CustomException as e:
        logger.warning(e, exc_info=True)
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
        logger.warning(e, exc_info=True)
        return f"{e.name}: {e.message}", 500


@blueprint.route('/metrics', methods=['get'])
@inject
def get_metrics(telemetrics_service: TelemetricsService = Provide[Container.telemetrics_service]):
    try:
        mission_id = request.args.get('mission_id', type=str)
        metrics_list = telemetrics_service.get_history(mission_id)
        return jsonify(metrics_list)
    except CustomException as e:
        logger.warning(e, exc_info=True)
        return f"{e.name}: {e.message}", 500
