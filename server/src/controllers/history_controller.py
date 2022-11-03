from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from src.container import Container
from src.exceptions.custom_exception import CustomException
from src.services.logging_service import LoggingService
from src.services.mission_service import MissionService
from src.services.telemetrics_service import TelemetricsService

blueprint = Blueprint('history', __name__)


@blueprint.route('/mission/range', methods=['get'])
@inject
def get_mission_range(mission_service: MissionService = Provide[Container.mission_service]):
    try:
        mission_id = request.args.get('id', type=str)
        logs_list = mission_service.get_mission_by_id(mission_id)
        return jsonify(logs_list)
    except CustomException as e:
        return f"{e.name}: {e.message}", 500


@blueprint.route('/mission/id', methods=['get'])
@inject
def get_mission(mission_service: MissionService = Provide[Container.mission_service]):
    try:
        start_timestamp_ms = request.args.get('start', type=int)
        end_timestamp_ms = request.args.get('end', type=int)
        missions = mission_service.get_missions_range(start_timestamp_ms, end_timestamp_ms)
        return jsonify(missions)
    except CustomException as e:
        return f"{e.name}: {e.message}", 500


@blueprint.route('/logs', methods=['get'])
@inject
def get_logs(logging_service: LoggingService = Provide[Container.logging_service]):
    try:
        mission_id = request.args.get('id', type=str)
        logs_list = logging_service.get_history(mission_id)
        return jsonify(logs_list)
    except CustomException as e:
        return f"{e.name}: {e.message}", 500


@blueprint.route('/metrics', methods=['get'])
@inject
def get_metrics(telemetrics_service: TelemetricsService = Provide[Container.telemetrics_service]):
    try:
        mission_id = request.args.get('id', type=str)
        metrics_list = telemetrics_service.get_history(mission_id)
        return jsonify(metrics_list)
    except CustomException as e:
        return f"{e.name}: {e.message}", 500
