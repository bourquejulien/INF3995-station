from flask import Blueprint, jsonify, request

from src.clients.abstract_swarm_client import AbstractSwarmClient
from src.exceptions.custom_exception import CustomException
from dependency_injector.wiring import inject, Provide
from src.container import Container
from src.services.command_service import CommandService

blueprint = Blueprint('discovery', __name__)


@blueprint.route('/uris', methods=['get'])
@inject
def uris(swarm_client: AbstractSwarmClient = Provide[Container.abstract_swarm_client]):
    try:
        return jsonify(swarm_client.uris), 200
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500


@blueprint.route('/connect', methods=['post'])
@inject
def connect(command_service: CommandService = Provide[Container.command_service],
            swarm_client: AbstractSwarmClient = Provide[Container.abstract_swarm_client]):
    try:
        command_service.connect(command_service.discover())
        return jsonify(swarm_client.uris), 200
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500


@blueprint.route('/disconnect', methods=['post'])
@inject
def disconnect(command_service: CommandService = Provide[Container.command_service]):
    try:
        command_service.disconnect()
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200


@blueprint.route('/enabled', methods=['get'])
@inject
def is_enabled(command_service: CommandService = Provide[Container.command_service]):
    try:
        return jsonify(command_service.is_enabled)
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
