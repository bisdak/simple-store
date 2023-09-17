"""Flasks CLI/Application entry point."""
import os

from simple_store import create_app, db
from simple_store.models.user import UserModel

app = create_app(os.getenv("FLASK_ENV", "development"))


@app.shell_context_processor
def shell():
    return {"db": db, "User": UserModel}
