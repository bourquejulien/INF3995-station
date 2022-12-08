from src.exceptions.custom_exception import CustomException
import io
from flask import url_for


def test_get_file(client, app, mocker):
    firmware_service_mock = mocker.patch('src.services.firmware_service')
    firmware_service_mock.get_file.return_value = 'test'

    with app.container.firmware_service.override(firmware_service_mock):
        response = client.get(url_for("firmware.get_file"),
                              query_string={'path': 'test'})

    firmware_service_mock.get_file.assert_called_once_with('test')

    assert response.text == 'test'
    assert response.status_code == 200


def test_get_file_error(client, app, mocker):
    firmware_service_mock = mocker.patch('src.services.firmware_service')
    firmware_service_mock.get_file.side_effect = CustomException('test', 'test')

    with app.container.firmware_service.override(firmware_service_mock):
        response = client.get(url_for("firmware.get_file"),
                              query_string={'path': 'test'})

    firmware_service_mock.get_file.assert_called_once_with('test')

    assert response.text == 'test: test'
    assert response.status_code == 500


def test_edit(client, app, mocker):
    firmware_service_mock = mocker.patch('src.services.firmware_service')
    firmware_service_mock.edit.return_value = 'test'

    with app.container.firmware_service.override(firmware_service_mock):
        response = client.post(url_for("firmware.edit"),
                               query_string={'path': 'test'},
                               data="test")

    firmware_service_mock.edit.assert_called_once_with('test', b'test')

    assert response.text == 'success'
    assert response.status_code == 200


def test_edit_error(client, app, mocker):
    firmware_service_mock = mocker.patch('src.services.firmware_service')
    firmware_service_mock.edit.side_effect = CustomException('test', 'test')

    with app.container.firmware_service.override(firmware_service_mock):
        response = client.post(url_for("firmware.edit"),
                               query_string={'path': 'test'},
                               data="test")

    firmware_service_mock.edit.assert_called_once_with('test', b'test')

    assert response.text == 'test: test'
    assert response.status_code == 500


def test_build_flash(client, app, mocker):
    firmware_service_mock = mocker.patch('src.services.firmware_service')
    firmware_service_mock.flash_repo.return_value = 'test'

    with app.container.firmware_service.override(firmware_service_mock):
        response = client.post(url_for("firmware.build_flash"))

    firmware_service_mock.flash_repo.assert_called_once()

    assert response.text == 'success'
    assert response.status_code == 200


def test_build_flash_error(client, app, mocker):
    firmware_service_mock = mocker.patch('src.services.firmware_service')
    firmware_service_mock.flash_repo.side_effect = CustomException('test', 'test')

    with app.container.firmware_service.override(firmware_service_mock):
        response = client.post(url_for("firmware.build_flash"))

    firmware_service_mock.flash_repo.assert_called_once()

    assert response.text == 'test: test'
    assert response.status_code == 500


def test_flash(client, app, mocker):
    firmware_service_mock = mocker.patch('src.services.firmware_service')
    firmware_service_mock.flash_data.return_value = 'test'
    data = dict(
        file=(io.BytesIO(b'test'), "test"),
    )

    with app.container.firmware_service.override(firmware_service_mock):
        response = client.post(url_for("firmware.flash"),
                               data=data,
                               content_type='multipart/form-data')

    firmware_service_mock.flash_data.assert_called_once()

    assert response.text == 'success'
    assert response.status_code == 200


def test_flash_error(client, app, mocker):
    firmware_service_mock = mocker.patch('src.services.firmware_service')
    firmware_service_mock.flash_data.side_effect = CustomException('test', 'test')
    data = dict(
        file=(io.BytesIO(b'test'), "test"),
    )

    with app.container.firmware_service.override(firmware_service_mock):
        response = client.post(url_for("firmware.flash"),
                               data=data,
                               content_type='multipart/form-data')

    firmware_service_mock.flash_data.assert_called_once()

    assert response.text == 'test: test'
    assert response.status_code == 500
