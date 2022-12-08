from src.exceptions.custom_exception import CustomException
from flask import url_for


def test_uris(client, app, mocker):
    jsonify_mock = mocker.patch('src.controllers.discover_controller.jsonify')
    jsonify_mock.return_value = ['test']

    with app.container.command_service.override(jsonify_mock):
        response = client.get(url_for("discovery.uris"))

    assert response.text == '["test"]\n'
    assert response.status_code == 200


def test_uris_error(client, app, mocker):
    jsonify_mock = mocker.patch('src.controllers.discover_controller.jsonify')
    jsonify_mock.side_effect = CustomException('test', 'test')

    with app.container.command_service.override(jsonify_mock):
        response = client.get(url_for("discovery.uris"))

    assert response.status_code == 500


def test_connect(client, app, mocker):
    connect_mock = mocker.patch('src.services.command_service')
    connect_mock.connect.return_value = ""

    with app.container.command_service.override(connect_mock):
        response = client.post(url_for("discovery.connect"))

    connect_mock.connect.assert_called_once()
    assert response.status_code == 200


def test_connect_error(client, app, mocker):
    connect_mock = mocker.patch('src.services.command_service')
    connect_mock.connect.side_effect = CustomException('test', 'test')

    with app.container.command_service.override(connect_mock):
        response = client.post(url_for("discovery.connect"))

    assert response.text == "test: test"
    assert response.status_code == 500


def test_disconnect(client, app, mocker):
    disconnect_mock = mocker.patch('src.services.command_service')
    disconnect_mock.disconnect.return_value = ""

    with app.container.command_service.override(disconnect_mock):
        response = client.post(url_for("discovery.disconnect"))

    disconnect_mock.disconnect.assert_called_once()
    assert response.status_code == 200


def test_disconnect_error(client, app, mocker):
    disconnect_mock = mocker.patch('src.services.command_service')
    disconnect_mock.disconnect.side_effect = CustomException('test', 'test')

    with app.container.command_service.override(disconnect_mock):
        response = client.post(url_for("discovery.disconnect"))

    assert response.text == "test: test"


def test_is_enabled(client, app, mocker):
    jsonify_mock = mocker.patch('src.controllers.discover_controller.jsonify')
    jsonify_mock.return_value = 'test'

    with app.container.command_service.override(jsonify_mock):
        response = client.get(url_for("discovery.is_enabled"))

    assert response.text == 'test'
    assert response.status_code == 200


def test_is_enabled_error(client, app, mocker):
    jsonify_mock = mocker.patch('src.controllers.discover_controller.jsonify')
    jsonify_mock.side_effect = CustomException('test', 'test')

    with app.container.command_service.override(jsonify_mock):
        response = client.get(url_for("discovery.is_enabled"))

    assert response.text == "test: test"
