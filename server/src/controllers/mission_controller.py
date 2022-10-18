from flask import Blueprint, request
from dependency_injector.wiring import inject, Provide
from src.container import Container
from src.exceptions.custom_exception import CustomException

blueprint = Blueprint('mission', __name__)


@blueprint.route('/start', methods=['POST'])
@inject
def start(command_service=Provide[Container.command_service]):
    try:
        command_service.start_mission(request)
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200


@blueprint.route('/end', methods=['POST'])
@inject
def end(command_service=Provide[Container.command_service]):
    try:
        command_service.end_mission(request)
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200
