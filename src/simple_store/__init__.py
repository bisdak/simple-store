from datetime import timezone
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_smorest import Api
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

from simple_store.utils.datetime_util import utc_now, dtaware_fromtimestamp
from simple_store.config import get_config

cors = CORS()
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()


def create_app(config_name):
    app = Flask("simple_store")
    app.config.from_object(get_config(config_name))

    from simple_store.resources.user import blp as UserBlueprint
    from simple_store.resources.store import blp as StoreBlueprint

    cors.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    api = Api(app)
    jwt = JWTManager(app)

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        # TODO: Read from a config file instead of hard-coding
        if identity == 1:
            return {"is_admin": True}
        return {"is_admin": False}

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        token = request.headers["Authorization"].split(" ")[1]
        return BlacklistedToken.check_blacklist(token)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "message": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(StoreBlueprint)
    return app


class BlacklistedToken(db.Model):
    """BlacklistedToken Model for storing JWT tokens."""

    __tablename__ = "token_blacklist"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, default=utc_now)
    expires_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, token, expires_at):
        self.token = token
        self.expires_at = dtaware_fromtimestamp(expires_at, use_tz=timezone.utc)

    def __repr__(self):
        return f"<BlacklistToken token={self.token}>"

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def check_blacklist(cls, token):
        exists = cls.query.filter_by(token=token).first()
        return True if exists else False

    @classmethod
    def delete_expired_token(cls):
        tokens = cls.query.all()
        for token in tokens:
            if token.expires_at < utc_now().replace(tzinfo=None):
                db.session.delete(token)
        db.session.commit()
