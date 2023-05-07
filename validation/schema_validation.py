from marshmallow import (
    fields,
    Schema,
    validate,
    ValidationError
)

class CreateNewUser(Schema):
    name = fields.Str(required=True)
    email_address = fields.Str(required=True)
    phone_number = fields.Str(required=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    type_user = fields.Str(required=True, validate=validate.OneOf(['ADMIN', 'USER']))


class LoginUser(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)
    
class AddProducts(Schema):
    item_name = fields.Str(required=True)
    quantity = fields.Int(required=True)
    description = fields.Str(required=True)