from simple_store import db
from simple_store.models.store import Store
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)

    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False
    )
    store = db.relationship("Store", back_populates="items")

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


class ItemModelSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Item
        include_relationships = True
        load_instance = True
