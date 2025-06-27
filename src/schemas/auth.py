from marshmallow import Schema, fields


class Login(Schema):
    login = fields.Str(required=True)
    password = fields.Str(required=True)
