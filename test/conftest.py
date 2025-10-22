import pytest
from app import app

app.config.update({
    "TESTING": True,
})

@pytest.fixture()
def client():
    return app.test_client()

@pytest.fixture()
def runner():
    return app.test_cli_runner()
