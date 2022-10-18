from flask import Blueprint, jsonify
from dependency_injector.wiring import inject, Provide
from src.container import Container

blueprint = Blueprint('', __name__)


@blueprint.route('/health')
def health():
    return 'healthy'


@blueprint.route('/is_simulation', methods=['GET'])
@inject
def run_mode(config=Provide[Container.config]):
    return jsonify(config['is_simulation'])
