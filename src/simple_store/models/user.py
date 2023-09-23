"""Class definition for User model."""
from datetime import timedelta, timezone
from uuid import uuid4

from flask import current_app
from sqlalchemy.ext.hybrid import hybrid_property

from simple_store import db, bcrypt
from simple_store.utils.datetime_util import (
    utc_now,
    get_local_utcoffset,
    make_tzaware,
    localized_dt_string,
)
from flask_jwt_extended import create_access_token


class User(db.Model):
    """User model for storing logon credentials and other details."""

    __tablename__ = "site_user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    registered_on = db.Column(db.DateTime, default=utc_now)
    admin = db.Column(db.Boolean, default=False)
    public_id = db.Column(db.String(36), unique=True, default=lambda: str(uuid4()))

    stores = db.relationship("Store", back_populates="user", lazy="dynamic")

    def __repr__(self):
        return (
            f"<User email={self.email}, public_id={self.public_id}, admin={self.admin}>"
        )

    @hybrid_property
    def registered_on_str(self):
        registered_on_utc = make_tzaware(
            self.registered_on, use_tz=timezone.utc, localize=False
        )
        return localized_dt_string(registered_on_utc, use_tz=get_local_utcoffset())

    @property
    def password(self):
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password):
        log_rounds = current_app.config.get("BCRYPT_LOG_ROUNDS")
        hash_bytes = bcrypt.generate_password_hash(password, log_rounds)
        self.password_hash = hash_bytes.decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_public_id(cls, public_id):
        return cls.query.filter_by(public_id=public_id).first()

    def create_access_token(self):
        token_age_h = current_app.config.get("TOKEN_EXPIRE_HOURS")
        token_age_m = current_app.config.get("TOKEN_EXPIRE_MINUTES")
        expire = timedelta(hours=token_age_h, minutes=token_age_m)
        if current_app.config["TESTING"]:
            expire = timedelta(seconds=5)
        return create_access_token(
            identity=self.public_id, expires_delta=expire, fresh=True
        )
