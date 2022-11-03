from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from src.container import Container
from src.exceptions.custom_exception import CustomException
from src.services.logging_service import LoggingService
from src.services.mapping_service import MappingService
from src.services.telemetrics_service import TelemetricsService

blueprint = Blueprint('drone-info', __name__)


@blueprint.route('/status', methods=['get'])
@inject
def status(telemetrics_service: TelemetricsService = Provide[Container.telemetrics_service]):
    return telemetrics_service.latest, 200


@blueprint.route('/getLogs', methods=['get'])
@inject
def get_logs_since(logging_service: LoggingService = Provide[Container.logging_service]):
    try:
        # TODO Change ID to since_timestamp
        since_timestamp_ms = request.args.get('id', type=int)
        logs_list = logging_service.get_since(since_timestamp_ms)
        return jsonify(logs_list)
    except CustomException as e:
        return f"{e.name}: {e.message}", 500


@blueprint.route('/metrics', methods=['get'])
@inject
def get_metrics_since(telemetrics_service: TelemetricsService = Provide[Container.telemetrics_service]):
    try:
        since_timestamp_ms = request.args.get('since', type=int)
        metrics_list = telemetrics_service.get_since(since_timestamp_ms)
        return jsonify(metrics_list)
    except CustomException as e:
        return f"{e.name}: {e.message}", 500


@blueprint.route('/maps', methods=['get'])
@inject
def get_map_by_id(mapping_service: MappingService = Provide[Container.mapping_service]):
    try:
        uri = request.args.get('uri', type=str)
        position_list = mapping_service.get_map(uri)
        return jsonify(position_list)
    except CustomException as e:
        return f"{e.name}: {e.message}", 500
