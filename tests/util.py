"""Shared functions and constants for unit tests."""
from flask import url_for

EMAIL = "new_user@email.com"
PASSWORD = "test12345"
BAD_REQUEST = "Input payload validation failed"
WWW_AUTH_NO_TOKEN = 'Bearer realm="registered_user@mydomain.com"'


def user_data(email, password):
    return {"email": email, "password": password}


def register_user(test_client, email=EMAIL, password=PASSWORD):
    return test_client.post(url_for("Users.register"), json=user_data(email, password))


def login_user(test_client, email=EMAIL, password=PASSWORD):
    return test_client.post(url_for("Users.login"), json=user_data(email, password))


def logout_user(test_client, access_token):
    return test_client.post(
        url_for("api.auth_logout"), headers={"Authorization": f"Bearer {access_token}"}
    )


def get_user(test_client, access_token):
    return test_client.get(
        url_for("Users.user"), headers={"Authorization": f"Bearer {access_token}"}
    )
