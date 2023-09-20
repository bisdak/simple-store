"""Unit tests for User model class."""


def test_create_access_token(user):
    access_token = user.create_access_token()
    assert isinstance(access_token, str)
