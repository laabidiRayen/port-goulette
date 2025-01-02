# ressources/port_facility.py

# from flask_smorest import Blueprint
# from flask.views import MethodView
# from flask import request
# from services.port_facility_service import (
#     get_all_port_facilities,
#     get_port_facility_by_id,
#     add_port_facility,
#     update_port_facility
# )

# blp = Blueprint("PortFacilities", "port_facilities", url_prefix="/facilities", description="Operations related to port facilities")

# @blp.route("/")
# class PortFacilityList(MethodView):
#     @blp.response(200, description="List of all port facilities")
#     def get(self):
#         """
#         Retrieve all port facilities.
#         """
#         facilities = get_all_port_facilities()
#         return [facility.to_dict() for facility in facilities], 200

#     @blp.arguments(schema=None)  # Replace `schema=None` with a proper Marshmallow schema if used
#     @blp.response(201, description="Port facility created successfully")
#     @blp.response(400, description="Invalid data provided")
#     def post(self):
#         """
#         Add a new port facility.
#         """
#         data = request.get_json()
#         name = data.get('name')
#         type = data.get('type')
#         capacity = data.get('capacity')

#         if not name or not type or not capacity:
#             return {"error": "Missing required fields"}, 400

#         facility = add_port_facility(name, type, capacity)
#         return {
#             "message": "Port facility created successfully",
#             "facility": facility.to_dict()
#         }, 201


# @blp.route("/<int:facility_id>")
# class PortFacilityDetail(MethodView):
#     @blp.response(200, description="Details of a specific port facility")
#     @blp.response(404, description="Port facility not found")
#     def get(self, facility_id):
#         """
#         Retrieve details of a specific port facility by ID.
#         """
#         facility = get_port_facility_by_id(facility_id)
#         if facility:
#             return facility.to_dict(), 200
#         return {"error": "Port facility not found"}, 404

#     @blp.arguments(schema=None)  # Replace `schema=None` with a proper Marshmallow schema if used
#     @blp.response(200, description="Port facility updated successfully")
#     @blp.response(404, description="Port facility not found")
#     def put(self, facility_id):
#         """
#         Update an existing port facility by ID.
#         """
#         data = request.get_json()
#         name = data.get('name')
#         type = data.get('type')
#         capacity = data.get('capacity')

#         if not name or not type or not capacity:
#             return {"error": "Missing required fields"}, 400

#         facility = update_port_facility(facility_id, name, type, capacity)
#         if facility:
#             return {
#                 "message": "Port facility updated successfully",
#                 "facility": facility.to_dict()
#             }, 200
#         return {"error": "Port facility not found"}, 404

from flask_smorest import Blueprint
from flask.views import MethodView
from flask import jsonify
from schemas import PortFacilitySchema
from services.port_facility_service import (
    get_all_port_facilities,
    get_port_facility_by_id,
    add_port_facility,
    update_port_facility
)

blp = Blueprint("PortFacilities", "port_facilities", url_prefix="/facilities", description="Operations related to port facilities")


@blp.route("/")
class PortFacilityList(MethodView):
    @blp.response(200, PortFacilitySchema(many=True), description="List of all port facilities")
    def get(self):
        """
        Retrieve all port facilities.
        """
        facilities = get_all_port_facilities()
        return facilities, 200

    @blp.arguments(PortFacilitySchema)
    @blp.response(201, PortFacilitySchema, description="Port facility created successfully")
    def post(self, data):
        """
        Add a new port facility.
        """
        try:
            name = data.get("name")
            description = data.get("description")
            operational_hours = data.get("operational_hours")
            
            facility = add_port_facility(name, description, operational_hours)
            return PortFacilitySchema().dump(facility), 201
        except Exception as e:
            return jsonify({"message": f"An unexpected error occurred: {str(e)}"}), 500


@blp.route("/<int:facility_id>")
class PortFacilityDetail(MethodView):
    @blp.response(200, PortFacilitySchema, description="Details of a specific port facility")
    @blp.response(404, description="Port facility not found")
    def get(self, facility_id):
        """
        Retrieve details of a specific port facility by ID.
        """
        try:
            facility = get_port_facility_by_id(facility_id)
            if facility:
                return {
                    "message": f"Port facility {facility_id} found",
                    "facility": PortFacilitySchema().dump(facility)
                }, 200
            return jsonify({"message": "Port facility not found"}), 404
        except Exception as e:
            return jsonify({"message": f"An unexpected error occurred: {str(e)}"}), 500

    @blp.arguments(PortFacilitySchema)
    @blp.response(200, PortFacilitySchema, description="Port facility updated successfully")
    @blp.response(404, description="Port facility not found")
    def put(self, data, facility_id):
        """
        Update an existing port facility.
        """
        try:
            # Extract individual fields from `data`
            name = data.get("name")
            description = data.get("description")
            operational_hours = data.get("operational_hours")

            # Update the facility
            facility = update_port_facility(facility_id, name, description, operational_hours)

            if facility:
                return {
                    "message": f"Port facility {facility_id} updated successfully",
                    "facility": PortFacilitySchema().dump(facility)
                }, 200
            return jsonify({"message": "Port facility not found"}), 404
        except Exception as e:
            return jsonify({"message": f"An unexpected error occurred: {str(e)}"}), 500