import logging

from flask import Blueprint, request
from dependency_injector.wiring import inject, Provide

from src.classes.position import Position
from src.container import Container
from src.exceptions.custom_exception import CustomException
from src.services.command_service import CommandService

logger = logging.getLogger(__name__)
blueprint = Blueprint("action", __name__)


@blueprint.route("/identify", methods=["post"])
@inject
def identify(command_service: CommandService = Provide[Container.command_service]):
    try:
        uris = request.json["uris"]
        command_service.identify(uris)
    except CustomException as e:
        logger.warning(e, exc_info=True)
        return "{}: {}".format(e.name, e.message), 500
    return "success", 200


@blueprint.route("/toggle_sync", methods=["post"])
@inject
def toggle_sync(command_service: CommandService = Provide[Container.command_service]):
    try:
        command_service.toggle_synchronization()
    except CustomException as e:
        logger.warning(e, exc_info=True)
        return "{}: {}".format(e.name, e.message), 500
    return "success", 200


@blueprint.route("/initial_positions", methods=["post"])
@inject
def initial_positions(command_service: CommandService = Provide[Container.command_service]):
    try:
        received_data: dict = request.json
        positions: list = []

        if len(received_data) == 0:
            return "Empty request", 202

        for key, value in received_data.items():
            positions.append((key, Position(value["x"], value["y"], 0), value["yaw"]))

        command_service.set_initial_positions(positions)

    except CustomException as e:
        logger.warning(e, exc_info=True)
        return "{}: {}".format(e.name, e.message), 500
    return "success", 200
