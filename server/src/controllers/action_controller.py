import logging

from flask import Blueprint, request
from dependency_injector.wiring import inject, Provide
from src.container import Container
from src.exceptions.custom_exception import CustomException
from src.services.command_service import CommandService

logger = logging.getLogger(__file__)
blueprint = Blueprint('action', __name__)


@blueprint.route('/identify', methods=['post'])
@inject
def identify(command_service: CommandService = Provide[Container.command_service]):
    try:
        uris = request.json["uris"]
        command_service.identify(uris)
    except CustomException as e:
        logger.warning(e, exc_info=True)
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200


@blueprint.route('/toggle_sync', methods=['post'])
@inject
def toggle_sync(command_service: CommandService = Provide[Container.command_service]):
    try:
        command_service.toggle_synchronization()
    except CustomException as e:
        logger.warning(e, exc_info=True)
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200
