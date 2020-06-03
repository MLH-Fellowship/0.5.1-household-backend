import pytest

from flask.testing import Client
from app import create_app


@pytest.fixture
def client():
    app = create_app()
    yield app.test_client()


def test_index_page(client: Client):
    resp = client.get("/")
    assert b'Hello World!' in resp.data
