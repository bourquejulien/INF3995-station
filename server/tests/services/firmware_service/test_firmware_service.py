from unittest import mock
import pytest
from src.services.firmware_service.firmware_service import FirmwareService


@pytest.fixture()
def firmware_service():
    with mock.patch.object(FirmwareService, "__init__", lambda x, y, z: None):
        firmware_service = FirmwareService(None, None)
        yield firmware_service


def test_flash_data(app, mocker, firmware_service):
    flash_mock = mocker.patch('src.services.firmware_service.no_compiler_firmware_service.NoCompilerFirmwareService.flash_data')

    firmware_service.flash_data([])

    flash_mock.assert_called_once_with([])


def test_edit(app, mocker, firmware_service):
    firmware_service.remote_compiler_client = mocker.Mock()

    firmware_service.edit('', [])

    firmware_service.remote_compiler_client.edit.assert_called_once_with('', [])


def test_get_file(app, mocker, firmware_service):
    firmware_service.remote_compiler_client = mocker.Mock()
    firmware_service.remote_compiler_client.get.return_value = 'test'

    result = firmware_service.get_file('')

    firmware_service.remote_compiler_client.get.assert_called_once_with('')
    assert result == 'test'
