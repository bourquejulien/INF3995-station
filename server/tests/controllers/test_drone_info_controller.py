from src.exceptions.custom_exception import CustomException
from flask import url_for


def test_get_logs_with_timestamp(client, app, mocker):
    logging_service_mock = mocker.patch('src.services.logging_service')
    logging_service_mock.get_since.return_value = ["test1"]
    logging_service_mock.get_history.return_value = ["test2"]

    with app.container.logging_service.override(logging_service_mock):
        response = client.get(url_for("drone-info.get_logs"),
                              query_string={
                                  'since_timestamp': 1000,
                                  'mission_id': 'test'})

    logging_service_mock.get_since.assert_called_once_with('test', 1000)
    logging_service_mock.get_history.assert_not_called()
    assert response.status_code == 200


def test_get_logs_without_timestamp(client, app, mocker):
    logging_service_mock = mocker.patch('src.services.logging_service')
    logging_service_mock.get_since.return_value = ["test1"]
    logging_service_mock.get_history.return_value = ["test2"]

    with app.container.logging_service.override(logging_service_mock):
        response = client.get(url_for("drone-info.get_logs"),
                              query_string={'mission_id': 'test'})

    logging_service_mock.get_since.assert_not_called()
    logging_service_mock.get_history.assert_called_with('test')
    assert response.status_code == 200


def test_get_logs_error(client, app, mocker):
    logging_service_mock = mocker.patch('src.services.logging_service')
    logging_service_mock.get_history.side_effect = CustomException('test', 'test')

    with app.container.logging_service.override(logging_service_mock):
        response = client.get(url_for("drone-info.get_logs"),
                              query_string={'mission_id': 'test'})

    logging_service_mock.get_history.assert_called_with('test')
    assert response.text == 'test: test'
    assert response.status_code == 500


def test_latest_metric(client, app, mocker):
    jsonify_mock = mocker.patch('src.controllers.drone_info_controller.jsonify')
    jsonify_mock.return_value = ['test']

    with app.container.logging_service.override(jsonify_mock):
        response = client.get(url_for("drone-info.get_latest_metric"))

    assert response.text == '["test"]\n'
    assert response.status_code == 200


def test_latest_metric_error(client, app, mocker):
    jsonify_mock = mocker.patch('src.controllers.drone_info_controller.jsonify')
    jsonify_mock.side_effect = CustomException('test', 'test')

    with app.container.logging_service.override(jsonify_mock):
        response = client.get(url_for("drone-info.get_latest_metric"))

    assert response.text == 'test: test'
    assert response.status_code == 500


def test_get_mao(client, app, mocker):
    mapping_service_mock = mocker.patch('src.services.mapping_service')
    mapping_service_mock.get_map.return_value = ["test"]

    with app.container.mapping_service.override(mapping_service_mock):
        response = client.get(url_for("drone-info.get_map"))

    assert response.text == '["test"]\n'
    assert response.status_code == 200


def test_get_mao_error(client, app, mocker):
    mapping_service_mock = mocker.patch('src.services.mapping_service')
    mapping_service_mock.get_map.side_effect = CustomException('test', 'test')

    with app.container.mapping_service.override(mapping_service_mock):
        response = client.get(url_for("drone-info.get_map"))

    assert response.text == 'test: test'
    assert response.status_code == 500


def test_get_latest_mao(client, app, mocker):
    mapping_service_mock = mocker.patch('src.services.mapping_service')
    mapping_service_mock.get_latest.return_value = ["test"]

    with app.container.mapping_service.override(mapping_service_mock):
        response = client.get(url_for("drone-info.get_latest_map"))

    assert response.text == '["test"]\n'
    assert response.status_code == 200


def test_get_latest_mao_error(client, app, mocker):
    mapping_service_mock = mocker.patch('src.services.mapping_service')
    mapping_service_mock.get_latest.side_effect = CustomException('test', 'test')

    with app.container.mapping_service.override(mapping_service_mock):
        response = client.get(url_for("drone-info.get_latest_map"))

    assert response.text == 'test: test'
    assert response.status_code == 500
