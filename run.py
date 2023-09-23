"""Flasks CLI/Application entry point."""
import os

from simple_store import create_app, db
from simple_store.models.item import Item
from simple_store.models.store import Store
from simple_store.models.user import User
from simple_store import BlacklistedToken

app = create_app(os.getenv("FLASK_ENV", "development"))


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "User": User,
        "BlacklistedToken": BlacklistedToken,
        "Item": Item,
        "Store": Store,
    }
