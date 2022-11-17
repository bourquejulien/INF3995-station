from flask import Blueprint, jsonify, request
from src.exceptions.custom_exception import CustomException
from dependency_injector.wiring import inject, Provide
from src.container import Container
from src.services.firmware_service.abstract_firmware_service import AbstractFirmwareService
from src.services.firmware_service.firmware_service import FirmwareService
from src.services.firmware_service.no_compiler_firmware_service import NoCompilerFirmwareService

blueprint = Blueprint('firmware', __name__)


@blueprint.route('/get_file', methods=['get'])
@inject
def get_file(firmware_service: AbstractFirmwareService = Provide[Container.firmware_service]):
    if not isinstance(firmware_service, FirmwareService):
        return "Remote compiler disabled", 500

    try:
        path = request.args.get('path')
        return jsonify(firmware_service.get_file(path)), 200
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500


@blueprint.route('/edit', methods=['post'])
@inject
def edit(firmware_service: AbstractFirmwareService = Provide[Container.firmware_service]):
    if not isinstance(firmware_service, FirmwareService):
        return "Remote compiler disabled", 500

    try:
        path = request.args.get('path')
        data = request.data
        firmware_service.edit(path, data)
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200


@blueprint.route('/build_flash', methods=['post'])
@inject
def build_flash(firmware_service: AbstractFirmwareService = Provide[Container.firmware_service]):
    if not isinstance(firmware_service, FirmwareService):
        return "Remote compiler disabled", 500

    try:
        firmware_service.flash_repo()
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200


@blueprint.route('/flash', methods=['post'])
@inject
def flash(firmware_service: AbstractFirmwareService = Provide[Container.firmware_service]):
    if not issubclass(firmware_service.__class__, NoCompilerFirmwareService):
        return "Firmware calls are not available, are you running in simulation mode?", 500

    try:
        data = request.data
        firmware_service.flash_data(data)
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200
