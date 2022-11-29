import logging

from flask import Blueprint, request, jsonify
from dependency_injector.wiring import inject, Provide
from src.container import Container
from src.exceptions.custom_exception import CustomException
from src.services.logging_service import LoggingService
from src.services.mapping_service import MappingService
from src.services.telemetrics_service import TelemetricsService

logger = logging.getLogger(__name__)
blueprint = Blueprint('drone-info', __name__)


@blueprint.route('/logs', methods=['get'])
@inject
def get_logs(logging_service: LoggingService = Provide[Container.logging_service]):
    try:
        mission_id = request.args.get("mission_id", type=str)
        since_timestamp_ms = request.args.get('since_timestamp', type=int)
        if since_timestamp_ms is not None:
            logs_list = logging_service.get_since(mission_id, since_timestamp_ms)
        else:
            logs_list = logging_service.get_history(mission_id)
        return jsonify(logs_list)
    except CustomException as e:
        logger.warning(e, exc_info=True)
        return f"{e.name}: {e.message}", 500

@blueprint.route('/latestMetric', methods=['get'])
@inject
def get_latest_metric(telemetrics_service: TelemetricsService = Provide[Container.telemetrics_service]):
    try:
        latest_metrics = telemetrics_service.latest
        return jsonify(latest_metrics)
    except CustomException as e:
        logger.warning(e, exc_info=True)
        return f"{e.name}: {e.message}", 500

@blueprint.route('/maps', methods=['get'])
@inject
def get_map(mapping_service: MappingService = Provide[Container.mapping_service]):
    try:
        map_list = mapping_service.get_map()
        return jsonify(map_list)
    except CustomException as e:
        logger.warning(e, exc_info=True)
        return f"{e.name}: {e.message}", 500

@blueprint.route('/latestMap', methods=['get'])
@inject
def get_latest_map(mapping_service: MappingService = Provide[Container.mapping_service]):
    try:
        map_list = mapping_service.get_latest()
        return jsonify(map_list)
    except CustomException as e:
        return f"{e.name}: {e.message}", 500