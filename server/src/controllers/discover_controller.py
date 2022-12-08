import logging

from flask import Blueprint, jsonify

from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.exceptions.custom_exception import CustomException
from dependency_injector.wiring import inject, Provide
from src.container import Container
from src.services.command_service import CommandService
from src.services.telemetrics_service import TelemetricsService

logger = logging.getLogger(__name__)
blueprint = Blueprint("discovery", __name__)


def _get_all_uris(
    swarm_client: AbstractSwarmClient = Provide[Container.abstract_swarm_client],
    telemetrics_service: TelemetricsService = Provide[Container.telemetrics_service],
):
    all_uris = list(telemetrics_service.latest.keys())
    connected_uris = swarm_client.uris
    return {uri: uri in connected_uris for uri in all_uris}


@blueprint.route("/uris", methods=["get"])
@inject
def uris():
    try:
        return jsonify(_get_all_uris()), 200
    except CustomException as e:
        logger.warning(e, exc_info=True)
        return "{}: {}".format(e.name, e.message), 500


@blueprint.route("/connect", methods=["post"])
@inject
def connect(command_service: CommandService = Provide[Container.command_service]):
    try:
        command_service.connect(command_service.discover())
        return jsonify(_get_all_uris()), 200
    except CustomException as e:
        logger.warning(e, exc_info=True)
        return "{}: {}".format(e.name, e.message), 500


@blueprint.route("/disconnect", methods=["post"])
@inject
def disconnect(command_service: CommandService = Provide[Container.command_service]):
    try:
        command_service.disconnect()
    except CustomException as e:
        logger.warning(e, exc_info=True)
        return "{}: {}".format(e.name, e.message), 500
    return "success", 200


@blueprint.route("/enabled", methods=["get"])
@inject
def is_enabled(command_service: CommandService = Provide[Container.command_service]):
    try:
        return jsonify(command_service.is_enabled)
    except CustomException as e:
        logger.warning(e, exc_info=True)
        return "{}: {}".format(e.name, e.message), 500
