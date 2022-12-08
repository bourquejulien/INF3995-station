from src.exceptions.custom_exception import CustomException
from flask import url_for

ERROR = CustomException("test", "test")


def test_identify(client, app, mocker):
    identify_mock = mocker.patch("src.services.command_service")
    identify_mock.identify.return_value = ""

    with app.container.command_service.override(identify_mock):
        response = client.post(url_for("action.identify"), json={"uris": ["test"]})

    identify_mock.identify.assert_called_once_with(["test"])
    assert response.status_code == 200


def test_identify_error(client, app, mocker):
    identify_mock = mocker.patch("src.services.command_service")
    identify_mock.identify.side_effect = ERROR

    with app.container.command_service.override(identify_mock):
        response = client.post(url_for("action.identify"), json={"uris": ["test"]})

    assert response.text == "test: test"
    assert response.status_code == 500


def test_toggle_sync(client, app, mocker):
    toggle_sync_mock = mocker.patch("src.services.command_service")
    toggle_sync_mock.toggle_synchronization.return_value = ""

    with app.container.command_service.override(toggle_sync_mock):
        response = client.post(url_for("action.toggle_sync"))

    toggle_sync_mock.toggle_synchronization.assert_called_once()
    assert response.status_code == 200


def test_toggle_sync_error(client, app, mocker):
    toggle_sync_mock = mocker.patch("src.services.command_service")
    toggle_sync_mock.toggle_synchronization.side_effect = ERROR

    with app.container.command_service.override(toggle_sync_mock):
        response = client.post(url_for("action.toggle_sync"))

    assert response.text == "test: test"
    assert response.status_code == 500


def test_initial_positions(client, app, mocker):
    initial_positions_mock = mocker.patch("src.services.command_service")
    initial_positions_mock.set_initial_positions.return_value = ""

    with app.container.command_service.override(initial_positions_mock):
        response = client.post(url_for("action.initial_positions"), json={"uri": {"x": 0, "y": 0, "yaw": 0}})

    initial_positions_mock.set_initial_positions.assert_called_once()
    assert response.status_code == 200


def test_initial_positions_empty_request(client, app, mocker):
    initial_positions_mock = mocker.patch("src.services.command_service")

    with app.container.command_service.override(initial_positions_mock):
        response = client.post(url_for("action.initial_positions"))

    assert response.status_code == 400


def test_initial_positions_error(client, app, mocker):
    initial_positions_mock = mocker.patch("src.services.command_service")
    initial_positions_mock.set_initial_positions.side_effect = ERROR

    with app.container.command_service.override(initial_positions_mock):
        response = client.post(url_for("action.initial_positions"), json={"uri": {"x": 0, "y": 0, "yaw": 0}})

    assert response.text == "test: test"
    assert response.status_code == 500
