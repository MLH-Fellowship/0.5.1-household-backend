import pytest

import os

from flask.testing import Client
from app import create_app

TEST_USER1_USERNAME = "Person 1"
TEST_USER1_EMAIL = "person1@example.com"
TEST_USER1_PASSWORD = "Test_passw0rd"

TEST_USER2_USERNAME = "Person 2"
TEST_USER2_EMAIL = "person2@example.com"
TEST_USER2_PASSWORD = "Test2_passs0rd"

TEST_USER3_USERNAME = "Person 3"
TEST_USER3_EMAIL = "person3@example.com"
TEST_USER3_PASSWORD = "Test3_passs0rd"

TEST_HOUSE_NAME = "house"
TEST_HOUSE_DESCRIPTION = "a house"

TEST_HOUSE_NEW_NAME = "house2"


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
def test_register_user_2(client: Client):
    resp = client.post(
        "/auth/register",
        json=dict(
            username=TEST_USER2_USERNAME,
            email=TEST_USER2_EMAIL,
            password=TEST_USER2_PASSWORD,
        ),
    )
    json = resp.get_json()
    assert json["msg"] == "Created a new user."
    assert json["status"] == "success"


@pytest.mark.serial
def test_register_user_3(client: Client):
    resp = client.post(
        "/auth/register",
        json=dict(
            username=TEST_USER3_USERNAME,
            email=TEST_USER3_EMAIL,
            password=TEST_USER3_PASSWORD,
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


def authenticate_user1(client: Client):
    return client.post(
        "/auth/login",
        json=dict(identifier=TEST_USER1_USERNAME, password=TEST_USER1_PASSWORD),
    ).get_json()["data"]


def authenticate_user2(client: Client):
    return client.post(
        "/auth/login",
        json=dict(identifier=TEST_USER2_USERNAME, password=TEST_USER2_PASSWORD),
    ).get_json()["data"]


def authenticate_user3(client: Client):
    return client.post(
        "/auth/login",
        json=dict(identifier=TEST_USER3_USERNAME, password=TEST_USER3_PASSWORD),
    ).get_json()["data"]


@pytest.mark.serial
def test_user_create_house(client: Client):
    auth = authenticate_user1(client)
    resp = client.post(
        "/house/add",
        json=dict(name=TEST_HOUSE_NAME, description=TEST_HOUSE_DESCRIPTION),
        headers={"Authorization": auth},
    )
    json_resp = resp.get_json()
    assert json_resp["status"] == "success"


@pytest.mark.serial
def test_user_can_get_houses(client: Client):
    auth = authenticate_user1(client)
    resp = client.get("/house/user", headers={"Authorization": auth})
    json_resp = resp.get_json()
    assert len(json_resp["data"]) > 0


@pytest.mark.serial
def test_user_generic_invite_link(client: Client):
    auth = authenticate_user1(client)
    resp = client.get("/house/user", headers={"Authorization": auth})
    json_resp = resp.get_json()
    house_1 = json_resp["data"][0]
    invite_link = client.get(
        "/house/{}/user/invite".format(house_1), headers={"Authorization": auth}
    )
    json_invite = invite_link.get_json()
    assert json_invite["status"] == "success"
    assert len(json_invite["data"]) > 5
    auth2 = authenticate_user2(client)
    joined = client.get(json_invite["data"], headers={"Authorization": auth2})
    assert joined.get_json()["status"] == "success"


@pytest.mark.serial
def test_user_update_house(client: Client):
    auth = authenticate_user1(client)
    resp = client.get("/house/user", headers={"Authorization": auth})
    json_resp = resp.get_json()
    house_1 = json_resp["data"][0]
    update_resp = client.post(
        "/house/update",
        json={"house_id": house_1, "name": TEST_HOUSE_NEW_NAME},
        headers={"Authorization": auth},
    )
    assert update_resp.get_json()["status"] == "success"
    auth2 = authenticate_user2(client)
    house_resp = client.get(
        "/house/{}/get".format(house_1), headers={"Authorization": auth2}
    )
    json_house = house_resp.get_json()
    assert json_house["status"] == "success"
    assert json_house["data"]["name"] == TEST_HOUSE_NEW_NAME
