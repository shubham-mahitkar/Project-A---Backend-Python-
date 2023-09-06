import pytest

from users.app import app


@pytest.fixture
def client():
    app = app({"TESTING": True})
    with app.test_client() as client:
        yield client