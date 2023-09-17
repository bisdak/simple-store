from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from simple_store.config import get_config

cors = CORS()
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name):
    app = Flask("simple_store")
    app.config.from_object(get_config(config_name))

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    api = Api(app)
    jwt = JWTManager(app)

    with app.app_context():
        from simple_store import models

        db.create_all()

    return app
