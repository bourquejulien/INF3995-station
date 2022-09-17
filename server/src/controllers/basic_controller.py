from flask import Blueprint
from flask import request
from src.services.basic_service import BasicService

blueprint = Blueprint('basic-blueprint', __name__)
basic_service = BasicService()


@blueprint.route('/init', methods=['POST'])
def init():
    basic_service.init()
    return 'success', 200


@blueprint.route('/takeoff', methods=['POST'])
def takeoff():
    basic_service.takeoff()
    return 'success', 200
