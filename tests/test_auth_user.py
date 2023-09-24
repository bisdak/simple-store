import time
from http import HTTPStatus
from flask import url_for

from tests.util import register_user, login_user, get_user

SUCCESS = "User created successfully."
EMAIL_ALREADY_EXISTS = "Email address is already registered."
INVALID_EMAIL = "Not a valid email address."
AUTH_NO_TOKEN = "Request does not contain an access token."
EXPIRED_TOKEN = "The token has expired."


def test_auth_user(client, db):
    register_user(client)
    response = login_user(client)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    response = get_user(client, access_token)
    assert response.status_code == HTTPStatus.OK
    assert "email" in response.json and response.json["email"] == "new_user@email.com"
    assert "admin" in response.json and response.json["admin"] == False
    assert "public_id" in response.json
    assert "registered_on" in response.json


def test_auth_user_no_token(client, db):
    response = client.get(url_for("Users.user"))
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json["message"] == AUTH_NO_TOKEN


def test_auth_user_expired_token(client, db):
    register_user(client)
    response = login_user(client)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    time.sleep(6)
    response = get_user(client, access_token)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json["message"] == EXPIRED_TOKEN
    assert response.json["error"] == "token_expired"
