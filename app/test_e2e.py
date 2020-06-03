import pytest

from flask.testing import Client
from app import create_app

TEST_USER1_USERNAME = "Person 1"
TEST_USER1_EMAIL = "person1@example.com"
TEST_USER1_PASSWORD = "Test_passw0rd"


@pytest.fixture
def client():
    app = create_app()
    yield app.test_client()


@pytest.mark.serial
def test_index_page(client: Client):
    resp = client.get("/")
    assert b'Hello World!' in resp.data


@pytest.mark.serial
def test_register_user(client: Client):
    resp = client.post("/auth/register", json=dict(
        username=TEST_USER1_USERNAME,
        email=TEST_USER1_EMAIL,
        password=TEST_USER1_PASSWORD
    ))
    json = resp.get_json()
    assert json["msg"] == "Created a new user."
