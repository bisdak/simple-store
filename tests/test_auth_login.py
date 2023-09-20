from http import HTTPStatus

from tests.util import register_user, login_user

SUCCESS = "User created successfully."
EMAIL_ALREADY_EXISTS = "Email address is already registered."
INVALID_EMAIL = "Not a valid email address."


def test_login(client, db):
    register_user(client)
    response = login_user(client)
    assert response.status_code == HTTPStatus.OK
    assert "access_token" in response.json


def test_login_email_does_not_exist(client, db):
    response = login_user(client)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
