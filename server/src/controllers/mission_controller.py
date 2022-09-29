from flask import Blueprint, request

from src.clients.abstract_swarm_client import AbstractSwarmClient

swarm_client: AbstractSwarmClient | None = None
blueprint = Blueprint('mission', __name__)


@blueprint.route('/start', methods=['POST'])
def start():
    swarm_client.start_mission()
    return 'success', 200


@blueprint.route('/end', methods=['POST'])
def end():
    swarm_client.end_mission()
    return 'success', 200
