from flask import Blueprint, request
from src.services.command_service import CommandService
from src.exceptions.custom_exception import CustomException

command_service = None | CommandService
blueprint = Blueprint('mission', __name__)


@blueprint.route('/start', methods=['POST'])
def start():
    try:
        command_service.start_mission(request)
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200


@blueprint.route('/end', methods=['POST'])
def end():
    try:
        command_service.end_mission(request)
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200
