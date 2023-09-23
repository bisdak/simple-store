from tests.util import register_store, login_user, register_user


def test_register_store(client, db):
    register_user(client)
    access_token = login_user(client).json["access_token"]
    response = register_store(client, access_token)
    assert response.status_code == 201
    assert "name" in response.json and response.json["name"] == "Amazon"
    assert "registered_by" in response.json and response.json["registered_by"] == 1
