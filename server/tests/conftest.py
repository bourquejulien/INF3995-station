import pytest
from app import create_app


@pytest.fixture()
def app():
    app, container = create_app()
    container.wire(modules=[".application", __name__], packages=[".controllers"], from_package="src")
    yield app
    container.unwire()
