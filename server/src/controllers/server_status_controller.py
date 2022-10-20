from flask import Blueprint, jsonify
from dependency_injector.wiring import inject, Provide
from src.container import Container

blueprint = Blueprint('', __name__)


@blueprint.route('/health', methods=['get'])
def health():
    return 'healthy', 200


@blueprint.route('/is_simulation', methods=['get'])
@inject
def is_simulation(config=Provide[Container.config]):
    return jsonify(config['is_simulation']), 200
