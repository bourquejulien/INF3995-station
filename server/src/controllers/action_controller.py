from flask import Blueprint, request
from src.services.command_service import CommandService
from src.exceptions.custom_exception import CustomException

command_service = CommandService | None
blueprint = Blueprint('action', __name__)


@blueprint.route('/identify', methods=['post'])
def identify():
    try:
        uris = request.json["uris"]
        command_service.identify(uris)
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200
