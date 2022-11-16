from flask import Blueprint, jsonify, request
from src.exceptions.custom_exception import CustomException
from dependency_injector.wiring import inject, Provide
from src.container import Container
from src.services.firmware_service.firmware_service import FirmwareService

blueprint = Blueprint('firmware', __name__)


@blueprint.route('/get_file', methods=['get'])
@inject
def get_file(firmware_service: FirmwareService = Provide[Container.firmware_service]):
    try:
        path = request.args.get('path')
        return jsonify(firmware_service.get_file(path)), 200
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500


@blueprint.route('/edit', methods=['post'])
@inject
def edit(firmware_service: FirmwareService = Provide[Container.firmware_service]):
    try:
        path = request.args.get('path')
        data = request.data
        firmware_service.edit(path, data)
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200


@blueprint.route('/build_flash', methods=['post'])
@inject
def build_flash(firmware_service: FirmwareService = Provide[Container.firmware_service]):
    try:
        firmware_service.flash_repo()
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200


@blueprint.route('/flash', methods=['post'])
@inject
def flash(firmware_service: FirmwareService = Provide[Container.firmware_service]):
    try:
        data = request.data
        firmware_service.flash_data(data)
    except CustomException as e:
        return "{}: {}".format(e.name, e.message), 500
    return 'success', 200
