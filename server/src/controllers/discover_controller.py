from flask import Blueprint, jsonify, request
from dependency_injector.wiring import inject, Provide
from src.container import Container

blueprint = Blueprint('discovery', __name__)


@blueprint.route('/discover', methods=['get'])
@inject
def discover(command_service=Provide[Container.command_service]):
    return jsonify(command_service.discover()), 200


@blueprint.route('/connect', methods=['post'])
@inject
def connect(command_service=Provide[Container.command_service]):
    uris = request.args.get('uris')
    command_service.connect(uris)
    return 'success', 200


@blueprint.route('/disconnect', methods=['get'])
@inject
def disconnect(command_service=Provide[Container.command_service]):
    command_service.disconnect()
    return 'success', 200
