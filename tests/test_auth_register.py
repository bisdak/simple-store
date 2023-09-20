from http import HTTPStatus

from simple_store.models.user import User
from tests.util import EMAIL, PASSWORD, register_user

SUCCESS = "User created successfully."
EMAIL_ALREADY_EXISTS = "Email address is already registered."
INVALID_EMAIL = "Not a valid email address."


def test_register(client, db):
    response = register_user(client)
    print(response)
    assert response.status_code == HTTPStatus.CREATED
    assert "message" in response.json and response.json["message"] == SUCCESS
    assert "access_token" in response.json


def test_register_email_already_registered(client, db):
    user = User(email=EMAIL, password=PASSWORD)
    user.save_to_db()
    response = register_user(client)
    assert response.status_code == HTTPStatus.CONFLICT
    assert (
        "message" in response.json and response.json["message"] == EMAIL_ALREADY_EXISTS
    )
    assert "access_token" not in response.json


def test_register_invalid_email(client):
    invalid_email = "hello"
    response = register_user(client, email=invalid_email)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert "errors" in response.json
    assert INVALID_EMAIL in response.json["errors"]["json"]["email"]
