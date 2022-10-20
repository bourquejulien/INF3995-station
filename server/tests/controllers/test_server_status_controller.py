from flask import url_for


def test_health(client, app):
    response = client.get(url_for(".health"))
    assert response.text == 'healthy'
    assert response.status_code == 200


def test_is_simulation(client, app):
    response = client.get(url_for("is_simulation"))
    assert response.text == "true\n"
    assert response.status_code == 200
