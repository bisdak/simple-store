from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from simple_store.models.item import Item, ItemModelSchema
from simple_store.schemas import ItemSchema
from flask_jwt_extended import jwt_required


blp = Blueprint("Items", "items", description="Operations on items")


@blp.route("/item/<string:name>")
class Item(MethodView):
    @jwt_required()
    @blp.response(200, ItemSchema)
    def get(self, name):
        item = Item.find_by_name(name)
        if item:
            item_schema = ItemModelSchema()
            return item_schema.dump(item), 200
        abort(404, message="Item not found")

    @jwt_required(fresh=True)
    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data, name):
        if Item.find_by_name(name):
            abort(400, message=f"An item with name {name} already exists.")

        item = Item(**item_data, name=name)

        try:
            item.save_to_db()
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the item.")

        return item
