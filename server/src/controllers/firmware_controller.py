import logging

from flask import Blueprint, request
from src.exceptions.custom_exception import CustomException
from dependency_injector.wiring import inject, Provide
from src.container import Container
from src.services.firmware_service.abstract_firmware_service import AbstractFirmwareService
from src.services.firmware_service.firmware_service import FirmwareService
from src.services.firmware_service.no_compiler_firmware_service import NoCompilerFirmwareService

logger = logging.getLogger(__name__)
blueprint = Blueprint('firmware', __name__)


@blueprint.route('/get_file', methods=['get'])
@inject
def get_file(firmware_service: AbstractFirmwareService = Provide[Container.firmware_service]):
    try:
        path = request.args.get('path')
        return firmware_service.get_file(path), 200
    except CustomException as e:
        logger.warning(e, exc_info=True)
        return "{}: {}".format(e.name, e.message), 500


@blueprint.route('/edit', methods=['post'])
@inject
def edit(firmware_service: AbstractFirmwareService = Provide[Container.firmware_service]):
    try:
        path = request.args.get('path')
        data = request.data
        firmware_service.edit(path, data)
    except CustomException as e:
        logger.warning(e, exc_info=True)
        return "{}: {}".format(e.name, e.message), 500
    return "success", 200


@blueprint.route('/build_flash', methods=['post'])
@inject
def build_flash(firmware_service: AbstractFirmwareService = Provide[Container.firmware_service]):
    try:
        firmware_service.flash_repo()
    except CustomException as e:
        logger.warning(e, exc_info=True)
        return "{}: {}".format(e.name, e.message), 500
    return "success", 200


@blueprint.route('/flash', methods=['post'])
@inject
def flash(firmware_service: AbstractFirmwareService = Provide[Container.firmware_service]):
    try:
        file = request.files['file']
        firmware_service.flash_data(file.stream.read())
    except CustomException as e:
        logger.warning(e, exc_info=True)
        return "{}: {}".format(e.name, e.message), 500
    return "success", 200
