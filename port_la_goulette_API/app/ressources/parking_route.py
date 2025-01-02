from flask_smorest import Blueprint
from flask.views import MethodView
from flask import jsonify, request
from models.parking import Parking
from schemas import ParkingSchema,BookingSchema
from extensions import db
from services.parking_service import (
    get_all_parking_spaces,
    get_parking_by_id,
    create_parking_space,
    update_parking_space,
    delete_parking_space,
    book_parking_space,
)

blp = Blueprint("Parkings", "parkings", url_prefix="/parkings", description="Parking operations")

@blp.route("/")
class ParkingList(MethodView):
    @blp.response(200, ParkingSchema(many=True))
    def get(self):
        """Retrieve all parking spaces."""
        return get_all_parking_spaces()

    @blp.arguments(ParkingSchema)
    @blp.response(201, ParkingSchema)
    def post(self, data):
        """Create a new parking space."""
        return create_parking_space(data)


@blp.route("/<int:parking_id>")
class ParkingDetail(MethodView):
    @blp.response(200, ParkingSchema, description="Details of a specific parking space")
    @blp.response(404, description="Parking space not found")
    def get(self, parking_id):
        """
        Retrieve details of a specific parking space.
        """
        try:
            parking = get_parking_by_id(parking_id)
            if parking:
                return {
                    "message": f"Parking space {parking_id} found",
                    "parking": ParkingSchema().dump(parking)
                }, 200
            response = jsonify({"message": "Parking space not found"})
            response.status_code = 404
            return response
        except Exception as e:
            return jsonify({"message": f"An unexpected error occurred: {str(e)}"}), 500

    @blp.arguments(ParkingSchema)
    @blp.response(200, ParkingSchema, description="Parking space updated successfully")
    @blp.response(404, description="Parking space not found")
    def put(self, data, parking_id):
        """
        Update an existing parking space.
        """
        try:
            parking = update_parking_space(parking_id, data)
            if parking:
                return {
                    "message": f"Parking space {parking_id} updated successfully",
                    "parking": ParkingSchema().dump(parking)
                }, 200
            response = jsonify({"message": "Parking space not found"})
            response.status_code = 404
            return response
        except Exception as e:
            return jsonify({"message": f"An unexpected error occurred: {str(e)}"}), 500

    @blp.response(200, description="Parking space deleted successfully")
    @blp.response(404, description="Parking space not found")
    def delete(self, parking_id):
        """
        Delete an existing parking space.
        """
        try:
            success = delete_parking_space(parking_id)
            if success:
                return {"message": f"Parking space {parking_id} deleted successfully"}, 200
            response = jsonify({"message": "Parking space not found"})
            response.status_code = 404
            return response
        except Exception as e:
            return jsonify({"message": f"An unexpected error occurred: {str(e)}"}), 500


@blp.route("/book")
class ParkingBooking(MethodView):
    @blp.arguments(BookingSchema)
    @blp.response(201, description="Parking space booked successfully")
    @blp.response(400, description="Parking space not available")
    def post(self, data):
        """Book a parking space."""
        parking = book_parking_space(data["parking_id"], data["user_id"])
        if parking:
            return {"message": "Parking space booked successfully"},201
        return {"error": "Parking space not available or does not exist"}, 400