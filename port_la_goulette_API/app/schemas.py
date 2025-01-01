from marshmallow import Schema, fields

# schemas for user 
class PlainUserSchema(Schema):
    user_id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)

class UserRegisterSchema(PlainUserSchema):
    pass

class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True)

class UserUpdateSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Email(required=True)



# Ship schema
class PlainShipSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    arrival_time = fields.DateTime(required=True)
    departure_time = fields.DateTime(allow_none=True)
    status = fields.Str(required=True, default="arrived")

class ShipCreateSchema(Schema):
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    arrival_time = fields.DateTime(required=True)  # Using custom DateTimeStringField
    departure_time = fields.DateTime(allow_none=True)  # Optional departure time

class ShipUpdateStatusSchema(Schema):
    status = fields.Str(required=True)  

# ShipLinkService schema for linking a ship to a service
class ShipLinkServiceSchema(Schema):
    ship_id = fields.Int(required=True)
    service_id = fields.Int(required=True)




# Service schemas
class PlainServiceSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    price = fields.Float(required=True)
    is_available = fields.Bool(default=True)

class ServiceCreateSchema(Schema):
    name = fields.Str(required=True)
    description = fields.Str(allow_none=True)
    price = fields.Float(required=True)
    is_available = fields.Bool(default=True)

class ServiceUpdateSchema(Schema):
    name = fields.Str(allow_none=True)
    description = fields.Str(allow_none=True)
    price = fields.Float(allow_none=True)
    is_available = fields.Bool(allow_none=True)
