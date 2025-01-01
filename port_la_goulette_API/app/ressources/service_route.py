# ressources/service.py

# from flask_smorest import Blueprint
# from flask.views import MethodView
# from services.db_service import get_all_services, get_service_by_id

# blp = Blueprint("Services", "services", url_prefix="/services", description="Operations related to services")

# @blp.route("/")
# class ServiceList(MethodView):
#     @blp.response(200, description="List of all services")
#     def get(self):
#         services = get_all_services()
#         return services


# @blp.route("/<int:service_id>")
# class ServiceDetail(MethodView):
#     @blp.response(200, description="Details of a specific service")
#     @blp.response(404, description="Service not found")
#     def get(self, service_id):
#         service = get_service_by_id(service_id)
#         if service:
#             return service
#         return {"message": "Service not found"}, 404

from flask_smorest import Blueprint
from flask.views import MethodView
from services.db_service import get_all_services, get_service_by_id, create_service, update_service
from schemas import PlainServiceSchema, ServiceCreateSchema, ServiceUpdateSchema
from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from flask import jsonify
blp = Blueprint("Services", "services", url_prefix="/services", description="Operations related to services")

@blp.route("/")
class ServiceList(MethodView):
    @blp.response(200, PlainServiceSchema(many=True), description="List of all services")
    def get(self):
        services = get_all_services()
        return services

    @blp.arguments(ServiceCreateSchema)
    @blp.response(201, PlainServiceSchema, description="Service created successfully")
    @blp.response(400, description="Invalid input data")
    def post(self, data):
        try:
            # Extract fields from the validated input
            name = data["name"]
            description = data.get("description")  # Optional field
            price = data["price"]
            is_available = data.get("is_available", True)  # Default to True if not provided

            # Call the service layer to create the service
            new_service = create_service({
                "name": name,
                "description": description,
                "price": price,
                "is_available": is_available
            })
            
            # Return the newly created service and a 201 status code
            return new_service, 201

        except ValidationError as e:
            response = jsonify({"error": str(e)})
            response.status_code = 400
            return response
        except Exception as e:
            response = jsonify({"error": f"An unexpected error occurred: {str(e)}"})
            response.status_code = 500
            return response


@blp.route("/<int:service_id>")
class ServiceDetail(MethodView):
    @blp.response(200, PlainServiceSchema, description="Details of a specific service")
    @blp.response(404, description="Service not found")
    def get(self, service_id):
        service = get_service_by_id(service_id)
        if service:
            return service
        return {"message": "Service not found"}, 404

    @blp.arguments(ServiceUpdateSchema)
    @blp.response(200, PlainServiceSchema, description="Service updated successfully")
    @blp.response(404, description="Service not found")
    def put(self, data, service_id):
        service = update_service(service_id, data)
        if service is None:
            return {"message": "Service not found"}, 404
        elif "error" in service:
            return {"message": service["error"]}, 400
        return {
            "message": "Service updated successfully",
            "service": service
        }, 200
