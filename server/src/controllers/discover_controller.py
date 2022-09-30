from flask import Blueprint, jsonify, request

from src.services.startup_service import StartupService

startupService: StartupService | None = None
blueprint = Blueprint('discovery', __name__)


@blueprint.route('/discover', methods=['get'])
def discover():
    return jsonify(startupService.drones_ids), 200


@blueprint.route('/connect', methods=['POST'])
def connect():
    uris = request.args.get('uris')
    startupService.connect(uris)
    return 'success', 200


@blueprint.route('/disconnect', methods=['get'])
def disconnect():
    startupService.disconnect()
    return 'success', 200
