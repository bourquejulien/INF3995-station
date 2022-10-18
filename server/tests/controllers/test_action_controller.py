from unittest import mock
from src.services.command_service import CommandService
from flask import url_for


def test_identify_error(client, app):
    identify_mock = mock.Mock(CommandService)
    identify_mock.identify.return_value = []

    with app.container.command_service.override(identify_mock):
        client.post(url_for("action.identify"), json={'uris': ['test']})

    identify_mock.identify.assert_called()
