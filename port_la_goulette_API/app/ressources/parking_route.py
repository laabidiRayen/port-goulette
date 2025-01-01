# ressources/parking.py

from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from models.parking import Parking
from services.parking_service import (
    get_parking_by_id,
    get_all_parking_spaces,
    book_parking_space
)

blp = Blueprint("Parkings", "parkings", url_prefix="/parkings", description="Operations related to parking spaces")

@blp.route("/")
class ParkingList(MethodView):
    @blp.response(200, description="List of all parking spaces")
    def get(self):
        """
        Retrieve all parking spaces.
        """
        parking_spaces = get_all_parking_spaces()
        return [space.to_dict() for space in parking_spaces], 200

    @blp.arguments(schema=None)  # Replace with proper schema if used
    @blp.response(201, description="Parking space booked successfully")
    @blp.response(400, description="Invalid data provided")
    def post(self):
        """
        Book a parking space.
        """
        data = request.get_json()
        parking_id = data.get('parking_id')
        user_id = data.get('user_id')
        
        if not parking_id or not user_id:
            return {"error": "Missing required fields"}, 400
        
        result = book_parking_space(parking_id, user_id)
        if result:
            return {"message": "Parking space booked successfully"}, 201
        return {"message": "Failed to book parking space"}, 400


@blp.route("/<int:parking_id>")
class ParkingDetail(MethodView):
    @blp.response(200, description="Details of a specific parking space")
    @blp.response(404, description="Parking space not found")
    def get(self, parking_id):
        """
        Retrieve details of a specific parking space by ID.
        """
        space = get_parking_by_id(parking_id)
        if space:
            return space.to_dict(), 200
        return {"error": "Parking space not found"}, 404

    @blp.arguments(schema=None)  # Replace with proper schema if used
    @blp.response(200, description="Parking space updated successfully")
    @blp.response(404, description="Parking space not found")
    def put(self, parking_id):
        """
        Update an existing parking space (e.g., mark as occupied or free).
        """
        data = request.get_json()
        space = Parking.query.get(parking_id)

        if not space:
            return {"message": "Parking space not found"}, 404
        
        space.status = data.get('status', space.status)
        space.save()
        
        return space.to_dict(), 200

    @blp.response(200, description="Parking space deleted successfully")
    @blp.response(404, description="Parking space not found")
    def delete(self, parking_id):
        """
        Delete a parking space by ID.
        """
        space = Parking.query.get(parking_id)

        if not space:
            return {"message": "Parking space not found"}, 404
        
        space.delete()
        return {"message": "Parking space deleted successfully"}, 200
