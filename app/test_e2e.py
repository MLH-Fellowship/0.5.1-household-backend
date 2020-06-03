import pytest

import os

from flask.testing import Client
from app import create_app

TEST_USER1_USERNAME = "Person 1"
TEST_USER1_EMAIL = "person1@example.com"
TEST_USER1_PASSWORD = "Test_passw0rd"

TEST_HOUSE_NAME = "house"
TEST_HOUSE_DESCRIPTION = "a house"


@pytest.fixture
def client():
    app = create_app()
    yield app.test_client()


@pytest.mark.serial
def test_index_page(client: Client):
    resp = client.get("/")
    assert b"Hello World!" in resp.data


@pytest.mark.serial
def test_register_user(client: Client):
    resp = client.post(
        "/auth/register",
        json=dict(
            username=TEST_USER1_USERNAME,
            email=TEST_USER1_EMAIL,
            password=TEST_USER1_PASSWORD,
        ),
    )
    json = resp.get_json()
    assert json["msg"] == "Created a new user."
    assert json["status"] == "success"


@pytest.mark.serial
def test_login_user(client: Client):
    resp = client.post(
        "/auth/login",
        json=dict(identifier=TEST_USER1_USERNAME, password=TEST_USER1_PASSWORD),
    )
    json = resp.get_json()
    assert json["status"] == "success"
    assert len(json["data"]) > 5


def authenticate(client: Client):
    return client.post(
        "/auth/login",
        json=dict(identifier=TEST_USER1_USERNAME, password=TEST_USER1_PASSWORD),
    ).get_json()["data"]


@pytest.mark.serial
def test_user_create_house(client: Client):
    auth = authenticate(client)
    resp = client.post(
        "/house/add",
        json=dict(name=TEST_HOUSE_NAME, description=TEST_HOUSE_DESCRIPTION),
        headers={"Authorization": auth},
    )
    json_resp = resp.get_json()
    assert json_resp["status"] == "success"
