from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from simple_store.models.store import Store as StoreModel
from simple_store.models.user import User as UserModel
from simple_store.schemas import StoreSchema

from flask_jwt_extended import jwt_required, get_jwt_identity

blp = Blueprint("Stores", "stores", description="Operations on stores")


@blp.route("/store/<string:name>", endpoint="store")
class Store(MethodView):
    @jwt_required()
    @blp.response(201, StoreSchema)
    def post(cls, name):
        """Register new store with current login user as owner"""
        if StoreModel.find_by_name(name):
            abort(400, message=f"A store with name '{name}' already exists.")

        public_id = get_jwt_identity()
        user = UserModel.find_by_public_id(public_id)
        store = StoreModel(name=name, registered_by=user.id)
        try:
            store.save_to_db()
        except SQLAlchemyError:
            abort(500, message="An error occured creating the store.")

        return store
