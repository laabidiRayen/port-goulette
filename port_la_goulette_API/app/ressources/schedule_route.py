

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
from schemas import ScheduleSchema, ScheduleUpdateSchema  # import the ScheduleSchema

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
    @blp.arguments(ScheduleUpdateSchema)
    @blp.response(200, description="Schedule updated successfully")
    @blp.response(404, description="Schedule not found")
    def put(self, data, schedule_id):
        """
        Update an existing schedule by ID.
        """
        # 'schedule_id' comes from the path parameter and 'data' comes from the body
        arrival_time = data.get('arrival_time')
        departure_time = data.get('departure_time')
        ship_id = data.get('ship_id')


        # Ensure ship_id exists in the Ships table if provided
        if ship_id and not Ship.query.get(ship_id):
            return {"error": "Invalid ship_id, no such ship exists."}, 400

        if not arrival_time or not departure_time:
            return {"error": "Missing required fields"}, 400

        try:
            # Convert the strings to datetime objects
            if isinstance(arrival_time, str):
                arrival_time = datetime.fromisoformat(arrival_time.rstrip("Z"))
            if isinstance(departure_time, str):
                departure_time = datetime.fromisoformat(departure_time.rstrip("Z"))
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
