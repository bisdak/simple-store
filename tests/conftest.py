"""Global pytest fixture"""
import pytest

from simple_store import create_app
from simple_store import db as database
from simple_store.models.user import User
from simple_store.models.store import Store
from simple_store.models.item import Item
from tests.util import EMAIL, PASSWORD, register_user, login_user, register_store


@pytest.fixture
def app():
    app = create_app("testing")
    return app


@pytest.fixture
def db(app, client, request):
    database.drop_all()
    database.create_all()
    database.session.commit()

    def fin():
        database.session.remove()

    request.addfinalizer(fin)
    return database


@pytest.fixture
def user(db):
    user = User(email=EMAIL, password=PASSWORD)
    db.session.add(user)
    db.session.commit()
    return user
