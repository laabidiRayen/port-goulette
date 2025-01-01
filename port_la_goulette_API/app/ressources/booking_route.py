# ressources/booking.py

from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from services.booking_service import (
    create_booking,
    get_bookings_for_ship,
    get_bookings_for_service,
    cancel_booking
)

blp = Blueprint("Bookings", "bookings", url_prefix="/bookings", description="Operations related to bookings")

@blp.route("/")
class BookingList(MethodView):
    @blp.response(200, description="List of all bookings for a ship or service")
    def get(self):
        """
        Retrieve all bookings for a ship or service.
        """
        # This could be further modified if you need to differentiate between bookings for ships or services.
        return {"message": "This route could be split further if needed for ships/services"}

    @blp.arguments(schema=None)  # Replace with proper schema if used
    @blp.response(201, description="Booking created successfully")
    @blp.response(400, description="Invalid data provided")
    def post(self):
        """
        Create a new booking for a ship or service.
        """
        data = request.get_json()
        ship_id = data.get('ship_id')
        service_id = data.get('service_id')
        user_id = data.get('user_id')
        date_time = data.get('date_time')

        if not ship_id or not service_id or not user_id or not date_time:
            return {"error": "Missing required fields"}, 400

        booking = create_booking(ship_id, service_id, user_id, date_time)
        return {"message": "Booking created successfully", "booking": booking.to_dict()}, 201


@blp.route("/ship/<int:ship_id>")
class BookingsForShip(MethodView):
    @blp.response(200, description="List of all bookings for a specific ship")
    def get(self, ship_id):
        """
        Retrieve all bookings for a specific ship.
        """
        bookings = get_bookings_for_ship(ship_id)
        return [booking.to_dict() for booking in bookings], 200


@blp.route("/service/<int:service_id>")
class BookingsForService(MethodView):
    @blp.response(200, description="List of all bookings for a specific service")
    def get(self, service_id):
        """
        Retrieve all bookings for a specific service.
        """
        bookings = get_bookings_for_service(service_id)
        return [booking.to_dict() for booking in bookings], 200


@blp.route("/<int:booking_id>")
class BookingDetail(MethodView):
    @blp.response(200, description="Booking canceled successfully")
    @blp.response(404, description="Booking not found")
    def delete(self, booking_id):
        """
        Cancel a booking by ID.
        """
        result = cancel_booking(booking_id)
        if result:
            return {"message": "Booking canceled successfully"}, 200
        return {"message": "Booking not found"}, 404
