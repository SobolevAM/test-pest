from marshmallow import Schema, fields


class UserByID(Schema):
    id = fields.Integer(required=True)


class User(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    age = fields.Integer(required=True)
    description = fields.Str(required=True)


class ResponseUser(Schema):
    id = fields.Integer()
    email = fields.Email()
    name = fields.Str()
    last_name = fields.Str()
    age = fields.Integer()
    description = fields.Str()


class UpdateUserInfo(Schema):
    name = fields.Str()
    last_name = fields.Str()
    age = fields.Integer()
    description = fields.Str()


class UserUpdateSecurity(Schema):
    email = fields.Email()
    password = fields.Str()