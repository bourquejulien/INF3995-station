from flask import Blueprint

blueprint = Blueprint('drone-info', __name__)


@blueprint.route('/status', methods=['get'])
def status():
    return {"uri1": "stubstatus1", "uri2": "stubstatus2"}, 200


@blueprint.route('/position', methods=['get'])
def position():
    return {"uri1": "stubposition1", "uri2": "stubposition2"}, 200
