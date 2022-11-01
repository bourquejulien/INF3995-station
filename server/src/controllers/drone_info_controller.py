from dependency_injector.wiring import inject, Provide
from src.container import Container
from src.exceptions.custom_exception import CustomException
from flask import Blueprint, request
from src.classes.events.log import generate_log

blueprint = Blueprint('drone-info', __name__)


@blueprint.route('/status', methods=['get'])
def status():
    return {"uri1": "stubstatus1", "uri2": "stubstatus2"}, 200


@blueprint.route('/position', methods=['GET'])
@inject
def get_position(command_service=Provide[Container.command_service]):
    try:
        json_pos = command_service.get_position()
    except CustomException as e:
        return json_pos.format(e.name, e.message), 500
    return json_pos, 200


@blueprint.route('/getLogs', methods=['get'])
def getLogs():
    args = request.args
    return [generate_log(args.get("mission_id"), "testlog", "INFO")], 200
