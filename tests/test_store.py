from simple_store.models.store import Store as StoreModel
from tests.util import (
    login_user,
    register_user,
    register_store,
    get_store,
    delete_store,
)

ALREADY_REGISTERED = "A store with name 'Amazon' already exists."
DELETION_FAILED = "Deletion allowed only for admin or store owner."


def test_register_store(client, db):
    register_user(client)
    access_token = login_user(client).json["access_token"]
    response = register_store(client, access_token)
    assert response.status_code == 201
    assert "name" in response.json and response.json["name"] == "Amazon"
    assert "registered_by" in response.json and response.json["registered_by"] == 1


def test_store_already_registered(client, db):
    register_user(client)
    access_token = login_user(client).json["access_token"]
    register_store(client, access_token)
    response = register_store(client, access_token)
    assert response.status_code == 400
    assert response.json["message"] == ALREADY_REGISTERED


def test_get_store(client, db):
    register_user(client)
    access_token = login_user(client).json["access_token"]
    register_store(client, access_token)
    response = get_store(client, "Amazon")
    assert response.status_code == 200
    assert response.json["name"] == "Amazon"


def test_store_not_registered(client, db):
    register_user(client)
    access_token = login_user(client).json["access_token"]
    register_store(client, access_token)
    response = get_store(client, "Lazada")
    assert response.status_code == 404
    assert response.json["message"] == "Store not found."


def test_delete_store(client, db):
    register_user(client)
    access_token = login_user(client).json["access_token"]
    register_store(client, access_token)
    stores = StoreModel.query.all()
    assert len(stores) == 1
    response = delete_store(client, access_token, "Amazon")
    stores = StoreModel.query.all()
    assert len(stores) == 0
    assert response.status_code == 200
    assert response.json["message"] == "Store deleted"


def test_attempt_to_delete_not_owned_store(client, db):
    register_user(client)
    access_token = login_user(client).json["access_token"]
    register_store(client, access_token)
    register_user(client, "other@email.com", "12345")
    access_token = login_user(client, "other@email.com", "12345").json["access_token"]
    response = delete_store(client, access_token, "Amazon")
    stores = StoreModel.query.all()
    assert len(stores) == 1
    assert response.status_code == 401
    assert response.json["message"] == DELETION_FAILED
