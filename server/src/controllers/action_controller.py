from flask import Blueprint, request
from dependency_injector.wiring import inject, Provide
from src.container import Container
from src.exceptions.custom_exception import CustomException

blueprint = Blueprint('action', __name__)


@blueprint.route('/identify', methods=['post'])
@inject
def identify(command_service=Provide[Container.command_service]):
    try:
        uris = request.json["uris"]
        command_service.identify(uris)
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200
