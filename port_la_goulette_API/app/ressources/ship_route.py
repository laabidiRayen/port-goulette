from flask_smorest import Blueprint
from flask.views import MethodView
from flask import jsonify
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError

from schemas import (
    PlainShipSchema,
    ShipCreateSchema,
    ShipUpdateStatusSchema,
)
from services.port_service import (
    get_all_ships,
    get_ship_by_id,
    get_ships_by_status,
    create_ship,
    update_ship_status,
    link_ship_to_service,
)

blp = Blueprint("Ships", "ships", url_prefix="/ships", description="Operations related to ships")


@blp.route("/")
class ShipList(MethodView):
    @blp.response(200, PlainShipSchema(many=True), description="List of all ships")
    def get(self):
        try:
            ships = get_all_ships()
            return ships
        except Exception as e:
            response = jsonify({"error": f"An unexpected error occurred: {str(e)}"})
            response.status_code = 500
            return response
    @blp.arguments(ShipCreateSchema)  # Use ShipCreateSchema to validate incoming data
    @blp.response(201, PlainShipSchema, description="Ship created successfully")
    @blp.response(400, description="Invalid input data")
    def post(self, data):
        try:
            # Extract fields from the validated input
            name = data["name"]
            type = data["type"]
            arrival_time = data["arrival_time"]
            departure_time = data.get("departure_time")  # Optional field
            status = data.get("status", "arrived")  # Default to "arrived" if not provided

            # Call the service layer to create the ship
            new_ship = create_ship(name, type, arrival_time, departure_time, status)
            return new_ship, 201
        except ValidationError as e:
            response = jsonify({"error": str(e)})
            response.status_code = 400
            return response
        except Exception as e:
            response = jsonify({"error": f"An unexpected error occurred: {str(e)}"})
            response.status_code = 500
            return response


@blp.route("/<int:ship_id>")
class ShipDetail(MethodView):
    @blp.response(200, PlainShipSchema, description="Details of a specific ship")
    @blp.response(404, description="Ship not found")
    def get(self, ship_id):
        try:
            ship = get_ship_by_id(ship_id)
            if ship:
                return {
                    "message": f"Ship {ship_id} found",
                    "ship": PlainShipSchema().dump(ship)
                }, 200
            response = jsonify({"message": "Ship not found"})
            response.status_code = 404
            return response
        except Exception as e:
            return jsonify({"message": f"An unexpected error occurred: {str(e)}"}), 500


@blp.route("/status/<string:status>")
class ShipsByStatus(MethodView):
    @blp.response(200, PlainShipSchema(many=True), description="List of ships by status")
    def get(self, status):
        try:
            ships = get_ships_by_status(status)
            if ships:
                return ships , 200
            response = jsonify({"message": "No ships found with the given status"})
            response.status_code = 404
            return response
        except ValidationError as e:
            response = jsonify({"error": str(e)})
            response.status_code = 400
            return response
        except Exception as e:
            response = jsonify({"error": f"An unexpected error occurred: {str(e)}"})
            response.status_code = 500
            return response


@blp.route("/<int:ship_id>/status")
class ShipStatusUpdate(MethodView):
    @blp.arguments(ShipUpdateStatusSchema)
    @blp.response(200, PlainShipSchema, description="Ship status updated successfully")
    @blp.response(404, description="Ship not found")
    def put(self, data, ship_id):
        try:
            new_status = data["status"]
            ship = update_ship_status(ship_id, new_status)
            if ship:
                return {
                    "message": f"Ship {ship_id} statue updated to {new_status}",
                    "ship": PlainShipSchema().dump(ship)
                }, 200
            response = jsonify({"message": "Ship not found"})
            response.status_code = 404
            return response
        except IntegrityError as e:
            response = jsonify({"error": f"Integrity error: {str(e)}"})
            response.status_code = 400
            return response
        except Exception as e:
            response = jsonify({"error": f"An unexpected error occurred: {str(e)}"})
            response.status_code = 500
            return response


@blp.route("/<int:ship_id>/service/<int:service_id>")
class ShipServiceLink(MethodView):
    @blp.response(200, PlainShipSchema, description="Ship linked to service successfully")
    @blp.response(404, description="Ship or service not found")
    def post(self, ship_id, service_id):
        try:
            # Link the ship to the service using the ship_id and service_id
            ship = link_ship_to_service(ship_id, service_id)
            if ship:
                return {
                    "message": f"Ship {ship_id} linked to service {service_id} successfully ",
                    "ship": PlainShipSchema().dump(ship)
                }, 200
            return {"message": "Ship or service not found"}, 404
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 500