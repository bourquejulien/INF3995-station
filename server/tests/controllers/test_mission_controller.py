from src.exceptions.custom_exception import CustomException
from src.classes.events.mission import generate_mission
from flask import url_for


def test_get_missions_with_mission_id(client, app, mocker):
    mission_service_mock = mocker.patch('src.services.mission_service')
    mission_service_mock.get_mission_by_id.return_value = generate_mission(False, 0, 2)
    mission_service_mock.get_last_missions.return_value = [generate_mission(False, 0, 2)]

    with app.container.mission_service.override(mission_service_mock):
        response = client.get(url_for("mission.get_missions"),
                              query_string={'mission_id': 'test'})

    mission_service_mock.get_mission_by_id.assert_called_once_with('test')
    mission_service_mock.get_last_missions.assert_not_called()
    assert response.status_code == 200


def test_get_missions_without_mission_id(client, app, mocker):
    mission_service_mock = mocker.patch('src.services.mission_service')
    mission_service_mock.get_mission_by_id.return_value = generate_mission(False, 0, 2)
    mission_service_mock.get_last_missions.return_value = [generate_mission(False, 0, 2)]

    with app.container.mission_service.override(mission_service_mock):
        response = client.get(url_for("mission.get_missions"))

    mission_service_mock.get_mission_by_id.assert_not_called()
    mission_service_mock.get_last_missions.assert_called_once()
    assert response.status_code == 200


def test_get_missions_error(client, app, mocker):
    mission_service_mock = mocker.patch('src.services.mission_service')
    mission_service_mock.get_last_missions.side_effect = CustomException('test', 'test')

    with app.container.mission_service.override(mission_service_mock):
        response = client.get(url_for("mission.get_missions"))

    mission_service_mock.get_last_missions.assert_called_once()

    assert response.text == 'test: test'
    assert response.status_code == 500


def test_get_current_mission(client, app, mocker):
    jsonify_mock = mocker.patch('src.controllers.mission_controller.jsonify')

    with app.container.mission_service.override(jsonify_mock):
        response = client.get(url_for("mission.current_mission"))

    jsonify_mock.assert_called_once()
    assert response.status_code == 200


def test_get_current_mission_error(client, app, mocker):
    jsonify_mock = mocker.patch('src.controllers.mission_controller.jsonify')
    jsonify_mock.side_effect = CustomException('test', 'test')

    with app.container.mission_service.override(jsonify_mock):
        response = client.get(url_for("mission.current_mission"))

    jsonify_mock.assert_called_once()
    assert response.text == 'test: test'
    assert response.status_code == 500


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


def test_force_end_mission(client, app, mocker):
    command_service_mock = mocker.patch('src.services.command_service')
    command_service_mock.force_end_mission.return_value = ""

    with app.container.command_service.override(command_service_mock):
        response = client.post(url_for("mission.force_end"))

    command_service_mock.force_end_mission.assert_called_once()
    assert response.status_code == 200


def test_force_end_mission_error(client, app, mocker):
    command_service_mock = mocker.patch('src.services.command_service')
    command_service_mock.force_end_mission.side_effect = CustomException('test', 'test')

    with app.container.command_service.override(command_service_mock):
        response = client.post(url_for("mission.force_end"))

    assert response.text == "test: test"
    assert response.status_code == 500


def test_return_to_base(client, app, mocker):
    command_service_mock = mocker.patch('src.services.command_service')
    command_service_mock.return_to_base.return_value = ""

    with app.container.command_service.override(command_service_mock):
        response = client.post(url_for("mission.return_to_base"))

    command_service_mock.return_to_base.assert_called_once()
    assert response.status_code == 200


def test_return_to_base_error(client, app, mocker):
    command_service_mock = mocker.patch('src.services.command_service')
    command_service_mock.return_to_base.side_effect = CustomException('test', 'test')

    with app.container.command_service.override(command_service_mock):
        response = client.post(url_for("mission.return_to_base"))

    assert response.text == "test: test"
    assert response.status_code == 500


def test_get_logs(client, app, mocker):
    logging_service_mock = mocker.patch('src.services.logging_service')
    logging_service_mock.get_history.return_value = ""

    with app.container.logging_service.override(logging_service_mock):
        response = client.get(url_for("mission.get_logs"),
                              query_string={'mission_id': 'test'})

    logging_service_mock.get_history.assert_called_once_with('test')
    assert response.status_code == 200


def test_get_logs_error(client, app, mocker):
    logging_service_mock = mocker.patch('src.services.logging_service')
    logging_service_mock.get_history.side_effect = CustomException('test', 'test')

    with app.container.logging_service.override(logging_service_mock):
        response = client.get(url_for("mission.get_logs"),
                              query_string={'mission_id': 'test'})

    assert response.text == "test: test"
    assert response.status_code == 500


def test_get_metrics(client, app, mocker):
    telemetrics_service_mock = mocker.patch('src.services.telemetrics_service')
    telemetrics_service_mock.get_history.return_value = ""

    with app.container.telemetrics_service.override(telemetrics_service_mock):
        response = client.get(url_for("mission.get_metrics"),
                              query_string={'mission_id': 'test'})

    telemetrics_service_mock.get_history.assert_called_once_with('test')
    assert response.status_code == 200


def test_get_logs_error(client, app, mocker):
    telemetrics_service_mock = mocker.patch('src.services.telemetrics_service')
    telemetrics_service_mock.get_history.side_effect = CustomException('test', 'test')

    with app.container.telemetrics_service.override(telemetrics_service_mock):
        response = client.get(url_for("mission.get_metrics"),
                              query_string={'mission_id': 'test'})

    assert response.text == "test: test"
    assert response.status_code == 500
