from simple_store import db
from simple_store.utils.datetime_util import utc_now


class Store(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime, default=utc_now)

    registered_by = db.Column(
        db.Integer, db.ForeignKey("site_user.id"), unique=False, nullable=False
    )
    items = db.relationship("Item", back_populates="store", lazy="dynamic")
    user = db.relationship("User", back_populates="stores")

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
