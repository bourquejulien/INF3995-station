from unittest import mock
import pytest
from src.services.firmware_service.no_compiler_firmware_service import NoCompilerFirmwareService


@pytest.fixture()
def ncf_service():
    command_service_mock = mock.Mock()
    client_mock = mock.Mock()

    yield NoCompilerFirmwareService(command_service_mock, client_mock)


def test_get_file(app, ncf_service):
    result = ncf_service.get_file("")
    assert result == b""
