from flask import Blueprint, request
from src.exceptions.custom_exception import CustomException
from src.services.command_service import CommandService

command_service: CommandService | None = None
blueprint = Blueprint('mission', __name__)


@blueprint.route('/start', methods=['POST'])
def start():
    try:
        command_service.start_mission([])
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200


@blueprint.route('/end', methods=['POST'])
def end():
    try:
        command_service.end_mission([])
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200


@blueprint.route('/force_end', methods=['POST'])
def force_end():
    try:
        command_service.force_end_mission([])
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200
