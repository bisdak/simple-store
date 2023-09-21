from simple_store import db
from simple_store.utils.datetime_util import utc_now
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Store(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, default=utc_now)

    registered_by = db.Column(
        db.Integer, db.ForeignKey("site_user.id"), unique=False, nullable=False
    )
    items = db.relationship("Item", back_populates="store", lazy="dynamic")


class StoreModelSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Store
        include_relationships = True
        load_instance = True
