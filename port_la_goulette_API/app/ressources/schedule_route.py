# ressources/schedule.py

# from flask_smorest import Blueprint
# from flask.views import MethodView
# from flask import request
# from services.schedule_service import (
#     get_all_schedules,
#     get_schedule_by_id,
#     add_schedule,
#     update_schedule,
#     delete_schedule
# )

# blp = Blueprint("Schedules", "schedules", url_prefix="/schedules", description="Operations related to schedules")

# @blp.route("/")
# class ScheduleList(MethodView):
#     @blp.response(200, description="List of all schedules")
#     def get(self):
#         """
#         Retrieve all schedules.
#         """
#         schedules = get_all_schedules()
#         return [schedule.to_dict() for schedule in schedules], 200

#     @blp.arguments(schema=None)  # Replace `schema=None` with a proper Marshmallow schema if used
#     @blp.response(201, description="Schedule created successfully")
#     @blp.response(400, description="Invalid data provided")
#     def post(self):
#         """
#         Create a new schedule.
#         """
#         data = request.get_json()
#         ship_id = data.get('ship_id')
#         arrival_time = data.get('arrival_time')
#         departure_time = data.get('departure_time')

#         if not ship_id or not arrival_time or not departure_time:
#             return {"error": "Missing required fields"}, 400

#         schedule = add_schedule(ship_id, arrival_time, departure_time)
#         return {
#             "message": "Schedule created successfully",
#             "schedule": schedule.to_dict()
#         }, 201


# @blp.route("/<int:schedule_id>")
# class ScheduleDetail(MethodView):
#     @blp.response(200, description="Details of a specific schedule")
#     @blp.response(404, description="Schedule not found")
#     def get(self, schedule_id):
#         """
#         Retrieve details of a specific schedule by ID.
#         """
#         schedule = get_schedule_by_id(schedule_id)
#         if schedule:
#             return schedule.to_dict(), 200
#         return {"error": "Schedule not found"}, 404

#     @blp.arguments(schema=None)  # Replace `schema=None` with a proper Marshmallow schema if used
#     @blp.response(200, description="Schedule updated successfully")
#     @blp.response(404, description="Schedule not found")
#     def put(self, schedule_id):
#         """
#         Update an existing schedule by ID.
#         """
#         data = request.get_json()
#         arrival_time = data.get('arrival_time')
#         departure_time = data.get('departure_time')

#         if not arrival_time or not departure_time:
#             return {"error": "Missing required fields"}, 400

#         schedule = update_schedule(schedule_id, arrival_time, departure_time)
#         if schedule:
#             return {
#                 "message": "Schedule updated successfully",
#                 "schedule": schedule.to_dict()
#             }, 200
#         return {"error": "Schedule not found"}, 404

#     @blp.response(200, description="Schedule deleted successfully")
#     def delete(self, schedule_id):
#         """
#         Delete a schedule by ID.
#         """
#         result = delete_schedule(schedule_id)
#         return result, 200

from datetime import datetime
from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from models.ship import Ship
from services.schedule_service import (
    get_all_schedules,
    get_schedule_by_id,
    add_schedule,
    update_schedule,
    delete_schedule,
    get_schedules_by_ship_id
)
from schemas import ScheduleSchema  # import the ScheduleSchema

blp = Blueprint("Schedules", "schedules", url_prefix="/schedules", description="Operations related to schedules")

@blp.route("/")
class ScheduleList(MethodView):
    @blp.response(200, ScheduleSchema(many=True), description="List of all schedules")
    def get(self):
        """
        Retrieve all schedules.
        """
        schedules = get_all_schedules()
        return schedules, 200

    @blp.arguments(ScheduleSchema)  # Use the ScheduleSchema to validate the input data
    @blp.response(201, ScheduleSchema, description="Schedule created successfully")
    @blp.response(400, description="Invalid data provided")
    def post(self, data):
        """
        Create a new schedule.
        """
        try:
            schedule = add_schedule(data["ship_id"], data["arrival_time"], data["departure_time"])
            return ScheduleSchema().dump(schedule), 201
        except ValueError as e:
            return {"error": str(e)}, 400  # Return error message if ship_id does not exist

@blp.route("/<int:schedule_id>")
class ScheduleDetail(MethodView):
    @blp.response(200, ScheduleSchema, description="Details of a specific schedule")
    @blp.response(404, description="Schedule not found")
    def get(self, schedule_id):
        """
        Retrieve details of a specific schedule by ID.
        """
        schedule = get_schedule_by_id(schedule_id)
        if schedule:
            return schedule, 200
        return {"error": "Schedule not found"}, 404

    @blp.response(200, ScheduleSchema, description="Schedule updated successfully")
    @blp.response(404, description="Schedule not found")
    def put(self, schedule_id):
        """
        Update an existing schedule by ID.
        """
        data = request.get_json()
        arrival_time = data.get('arrival_time')
        departure_time = data.get('departure_time')
        ship_id = data.get('ship_id')  # Add ship_id to the validation if provided

        # Ensure ship_id exists in the Ships table if provided
        if ship_id and not Ship.query.get(ship_id):
            return {"error": "Invalid ship_id, no such ship exists."}, 400

        if not arrival_time or not departure_time:
            return {"error": "Missing required fields"}, 400

        try:
            # Convert the strings to datetime objects
            arrival_time = datetime.fromisoformat(arrival_time.rstrip("Z"))  # Removing 'Z' if present
            departure_time = datetime.fromisoformat(departure_time.rstrip("Z"))  # Removing 'Z' if present
            schedule = update_schedule(schedule_id, arrival_time, departure_time, ship_id)
            if schedule:
                return {
                    "message": "Schedule updated successfully",
                    "schedule": ScheduleSchema().dump(schedule)  # Or schedule schema if using Marshmallow
                }, 200
            return {"error": "Schedule not found"}, 404
        except ValueError as e:
            return {"error": str(e)}, 400  # Return error if there is any problem in the update process


    @blp.response(200, description="Schedule deleted successfully")
    def delete(self, schedule_id):
        """
        Delete a schedule by ID.
        """
        result = delete_schedule(schedule_id)
        return result, 200


@blp.route("/ship/<int:ship_id>")
class ScheduleByShip(MethodView):
    @blp.response(200, ScheduleSchema(many=True), description="Schedules for a specific ship")
    @blp.response(404, description="No schedules found for the given ship")
    def get(self, ship_id):
        """
        Retrieve schedules for a specific ship by ship_id.
        """
        schedules = get_schedules_by_ship_id(ship_id)
        if schedules:
            return ScheduleSchema(many=True).dump(schedules), 200
        return {"error": "No schedules found for this ship"}, 404
