from flask import Blueprint

from src.services.command_service import CommandService

command_service: CommandService | None = None
blueprint = Blueprint('mission', __name__)


@blueprint.route('/start', methods=['POST'])
def start():
    command_service.start_mission([])
    return 'success', 200


@blueprint.route('/end', methods=['POST'])
def end():
    command_service.end_mission([])
    return 'success', 200


@blueprint.route('/force_end', methods=['POST'])
def force_end():
    command_service.force_end_mission([])
    return 'success', 200
