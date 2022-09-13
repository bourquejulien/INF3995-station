from flask import Blueprint
from flask import request

blueprint = Blueprint('basic-blueprint', __name__)


@blueprint.route('/init', methods=['POST'])
def init():
    print('Init')
    return 'success', 200


@blueprint.route('/takeoff', methods=['POST'])
def takeoff():
    data = request.form
    print(data.values())

    return 'success', 200
