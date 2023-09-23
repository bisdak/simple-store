from marshmallow import Schema, fields


class PlainUserSchema(Schema):
    id = fields.Int()
    email = fields.Email(required=True)
    password = fields.Str(load_only=True)


class UserSchema(Schema):
    id = fields.Int()
    email = fields.Email()
    registered_on = fields.DateTime()
    admin = fields.Bool()
    public_id = fields.Str()


class PlainItemSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)


class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class ItemSchema(PlainItemSchema):
    store_id = fields.Int(required=True, load_only=True)
    store = fields.Nested(PlainItemSchema(), dumpy_only=True)


class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()


class StoreSchema(PlainStoreSchema):
    registered_on = fields.DateTime(dump_only=True)
    registered_by = fields.Int(dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
