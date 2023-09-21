import time
from http import HTTPStatus

from simple_store import BlacklistedToken
from tests.util import register_user, login_user, logout_user

SUCCESS = "Successfully logged out."


def test_logout(client, db):
    register_user(client)
    response = login_user(client)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    blacklist = BlacklistedToken.query.all()
    assert len(blacklist) == 0
    response = logout_user(client, access_token)
    assert response.status_code == HTTPStatus.OK
    assert "message" in response.json and response.json["message"] == SUCCESS
    blacklist = BlacklistedToken.query.all()
    assert len(blacklist) == 1
    assert access_token == blacklist[0].token


def test_delete_expired_token_when_logged_out(client, db):
    register_user(client)
    response = login_user(client)
    assert "access_token" in response.json
    old_access_token = response.json["access_token"]
    blacklist = BlacklistedToken.query.all()
    assert len(blacklist) == 0
    response = logout_user(client, old_access_token)
    assert response.status_code == HTTPStatus.OK
    assert "message" in response.json and response.json["message"] == SUCCESS
    blacklist = BlacklistedToken.query.all()
    assert len(blacklist) == 1
    assert old_access_token == blacklist[0].token
    time.sleep(6)
    response = login_user(client)
    new_access_token = response.json["access_token"]
    response = logout_user(client, new_access_token)
    blacklist = BlacklistedToken.query.all()
    assert len(blacklist) == 1
    assert old_access_token != blacklist[0].token
