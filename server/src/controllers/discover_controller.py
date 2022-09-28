from flask import Blueprint, jsonify, request

from src.services.persistent_service import PersistentService

persistentService: PersistentService | None = None
blueprint = Blueprint('basic-blueprint', __name__)


@blueprint.route('/discover', methods=['get'])
def discover():
    return jsonify(persistentService.drones_ids), 200


@blueprint.route('/connect', methods=['POST'])
def connect():
    uri = request.args.get('uri')
    persistentService.connect(uri)
    return 'success', 200


@blueprint.route('/disconnect', methods=['get'])
def disconnect():
    persistentService.disconnect()
    return 'success', 200
