from src.exceptions.custom_exception import CustomException
from src.classes.events.mission import generate_mission
from flask import url_for


def test_start_mission(client, app, mocker):
    start_mission_mock = mocker.patch('src.services.command_service')
    start_mission_mock.start_mission.return_value = generate_mission(False, 0, 2)

    with app.container.command_service.override(start_mission_mock):
        response = client.post(url_for("mission.start"))

    start_mission_mock.start_mission.assert_called_once()
    assert response.status_code == 200


def test_start_mission_error(client, app, mocker):
    start_mission_mock = mocker.patch('src.services.command_service')
    start_mission_mock.start_mission.side_effect = CustomException('test', 'test')

    with app.container.command_service.override(start_mission_mock):
        response = client.post(url_for("mission.start"))

    assert response.text == '"error": "test: test"'
    assert response.status_code == 500


def test_end_mission(client, app, mocker):
    end_mission_mock = mocker.patch('src.services.command_service')
    end_mission_mock.end_mission.return_value = ""

    with app.container.command_service.override(end_mission_mock):
        response = client.post(url_for("mission.end"))

    end_mission_mock.end_mission.assert_called_once()
    assert response.status_code == 200


def test_end_mission_error(client, app, mocker):
    end_mission_mock = mocker.patch('src.services.command_service')
    end_mission_mock.end_mission.side_effect = CustomException('test', 'test')

    with app.container.command_service.override(end_mission_mock):
        response = client.post(url_for("mission.end"))

    assert response.text == "test: test"
    assert response.status_code == 500
