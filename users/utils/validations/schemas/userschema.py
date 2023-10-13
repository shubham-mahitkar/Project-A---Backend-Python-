from marshmallow import fields, Schema
from marshmallow.validate import Length, OneOf
from users import constants
from users.utils.util import validate_name, validate_email


class UserSchema(Schema):
    id = fields.Integer(required=False)
    name = fields.String(required=True, validate=[validate_name, Length(max=12)])
    email = fields.Email(required=True, validate=validate_email)
    password = fields.String(required=False)
    application = fields.List(fields.String(), required=True)
