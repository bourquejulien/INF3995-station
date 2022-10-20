from src.exceptions.custom_exception import CustomException
from flask import url_for


def test_identify(client, app, mocker):
    identify_mock = mocker.patch('src.services.command_service')
    identify_mock.identify.return_value = ""

    with app.container.command_service.override(identify_mock):
        response = client.post(url_for("action.identify"), json={'uris': ['test']})

    identify_mock.identify.assert_called_once_with(['test'])
    assert response.status_code == 200


def test_identify_error(client, app, mocker):
    identify_mock = mocker.patch('src.services.command_service')
    identify_mock.identify.side_effect = CustomException('test', 'test')

    with app.container.command_service.override(identify_mock):
        response = client.post(url_for("action.identify"), json={'uris': ['test']})

    assert response.text == "test: test"
    assert response.status_code == 500
