# ressources/booking.py

from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request, jsonify
from schemas import BookingSchema  # Assuming you have a schema for Booking
from services.booking_service import (
    create_booking,
    get_bookings_for_ship,
    get_bookings_for_service,
    cancel_booking,
    get_all_bookings
)

blp = Blueprint("Bookings", "bookings", url_prefix="/bookings", description="Operations related to bookings")

# Route to list all bookings (could be for any ship or service)
@blp.route("/")
class BookingList(MethodView):
    @blp.response(200, BookingSchema(many=True), description="List of all bookings")
    def get(self):
        """
        Retrieve all bookings for a ship or service.
        """
        bookings = get_all_bookings() 
        return bookings, 200

    @blp.arguments(BookingSchema)
    @blp.response(201, BookingSchema, description="Booking created successfully")
    def post(self, data):
        """
        Create a new booking.
        """
        try:
            booking = create_booking(data)  # Pass data to create a booking
            return booking, 201
        except Exception as e:
            return jsonify({"message": f"An unexpected error occurred: {str(e)}"}), 500


# Route for bookings related to a specific ship
@blp.route("/ship/<int:ship_id>")
class BookingsForShip(MethodView):
    @blp.response(200, BookingSchema(many=True), description="List of all bookings for a specific ship")
    def get(self, ship_id):
        """
        Retrieve all bookings for a specific ship.
        """
        bookings = get_bookings_for_ship(ship_id)
        return bookings, 200


# Route for bookings related to a specific service
@blp.route("/service/<int:service_id>")
class BookingsForService(MethodView):
    @blp.response(200, BookingSchema(many=True), description="List of all bookings for a specific service")
    def get(self, service_id):
        """
        Retrieve all bookings for a specific service.
        """
        bookings = get_bookings_for_service(service_id)
        return bookings, 200


# Route to cancel a specific booking
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
