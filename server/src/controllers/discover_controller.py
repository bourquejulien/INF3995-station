from flask import Blueprint, jsonify, request
from src.exceptions.custom_exception import CustomException
from dependency_injector.wiring import inject, Provide
from src.container import Container

blueprint = Blueprint('discovery', __name__)


@blueprint.route('/discover', methods=['get'])
@inject
def discover(command_service=Provide[Container.command_service]):
    try:
        return jsonify(command_service.discover()), 200
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200


@blueprint.route('/connect', methods=['post'])
@inject
def connect(command_service=Provide[Container.command_service]):
    try:
        uris = request.args.get('uris')
        command_service.connect(uris)
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200


@blueprint.route('/disconnect', methods=['post'])
@inject
def disconnect(command_service=Provide[Container.command_service]):
    try:
        command_service.disconnect()
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200
