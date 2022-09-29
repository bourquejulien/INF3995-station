from flask import Blueprint, request

from src.services.command_service import CommandService

command_service: CommandService | None
blueprint = Blueprint('action', __name__)


@blueprint.route('/identify', methods=['post'])
def identify():
    uris = request.json["uris"]
    command_service.identify(uris)
    return 'success', 200
