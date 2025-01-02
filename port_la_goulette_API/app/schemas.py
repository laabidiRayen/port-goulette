from datetime import datetime
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
    services = fields.Nested("PlainServiceSchema", many=True)  # Nested schema for services

class ShipCreateSchema(Schema):
    name = fields.Str(required=True)
    type = fields.Str(required=True)
    arrival_time = fields.DateTime(required=True)  # Using custom DateTimeStringField
    departure_time = fields.DateTime(allow_none=True)  # Optional departure time

class ShipUpdateStatusSchema(Schema):
    status = fields.Str(required=True)  



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



# feedback schemas
class FeedbackSchema(Schema):
    id = fields.Int(dump_only=True)  # id should only be included in the response
    user_id = fields.Int(required=True)
    message = fields.Str(required=True)
    rating = fields.Int()
    created_at = fields.DateTime(dump_only=True)  # created_at should be auto-generated

class FeedbackInputSchema(Schema):
    user_id = fields.Int(required=True)
    message = fields.Str(required=True)
    rating = fields.Int(required=False)  



# parking schemas
class ParkingSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    capacity = fields.Int(required=True)
    available_slots = fields.Int(required=True)
    price_per_hour = fields.Float(required=True)

class BookingSchema(Schema):
    parking_id = fields.Int(required=True, description="The ID of the parking space to book")
    user_id = fields.Int(required=True, description="The ID of the user booking the parking space")



# port_facility shcemas
class PortFacilitySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    description = fields.Str()
    operational_hours = fields.Str()



# booking schemas 
class BookingSchema(Schema):
    id = fields.Int()
    user_id = fields.Int()
    service_id = fields.Int()
    booking_date = fields.Method("serialize_booking_date")

    def serialize_booking_date(self, obj):
        # Ensure the booking_date is a datetime object before calling isoformat
        if isinstance(obj.booking_date, datetime):
            return obj.booking_date.isoformat()
        return obj.booking_date  



#Schedule Schemas
class ScheduleSchema(Schema):
    id = fields.Int(dump_only=True)
    ship_id = fields.Int(required=True)
    departure_time = fields.DateTime(required=True)
    arrival_time = fields.DateTime(required=True)