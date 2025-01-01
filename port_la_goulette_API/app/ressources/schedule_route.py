# ressources/schedule.py

from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from services.schedule_service import (
    get_all_schedules,
    get_schedule_by_id,
    add_schedule,
    update_schedule,
    delete_schedule
)

blp = Blueprint("Schedules", "schedules", url_prefix="/schedules", description="Operations related to schedules")

@blp.route("/")
class ScheduleList(MethodView):
    @blp.response(200, description="List of all schedules")
    def get(self):
        """
        Retrieve all schedules.
        """
        schedules = get_all_schedules()
        return [schedule.to_dict() for schedule in schedules], 200

    @blp.arguments(schema=None)  # Replace `schema=None` with a proper Marshmallow schema if used
    @blp.response(201, description="Schedule created successfully")
    @blp.response(400, description="Invalid data provided")
    def post(self):
        """
        Create a new schedule.
        """
        data = request.get_json()
        ship_id = data.get('ship_id')
        arrival_time = data.get('arrival_time')
        departure_time = data.get('departure_time')

        if not ship_id or not arrival_time or not departure_time:
            return {"error": "Missing required fields"}, 400

        schedule = add_schedule(ship_id, arrival_time, departure_time)
        return {
            "message": "Schedule created successfully",
            "schedule": schedule.to_dict()
        }, 201


@blp.route("/<int:schedule_id>")
class ScheduleDetail(MethodView):
    @blp.response(200, description="Details of a specific schedule")
    @blp.response(404, description="Schedule not found")
    def get(self, schedule_id):
        """
        Retrieve details of a specific schedule by ID.
        """
        schedule = get_schedule_by_id(schedule_id)
        if schedule:
            return schedule.to_dict(), 200
        return {"error": "Schedule not found"}, 404

    @blp.arguments(schema=None)  # Replace `schema=None` with a proper Marshmallow schema if used
    @blp.response(200, description="Schedule updated successfully")
    @blp.response(404, description="Schedule not found")
    def put(self, schedule_id):
        """
        Update an existing schedule by ID.
        """
        data = request.get_json()
        arrival_time = data.get('arrival_time')
        departure_time = data.get('departure_time')

        if not arrival_time or not departure_time:
            return {"error": "Missing required fields"}, 400

        schedule = update_schedule(schedule_id, arrival_time, departure_time)
        if schedule:
            return {
                "message": "Schedule updated successfully",
                "schedule": schedule.to_dict()
            }, 200
        return {"error": "Schedule not found"}, 404

    @blp.response(200, description="Schedule deleted successfully")
    def delete(self, schedule_id):
        """
        Delete a schedule by ID.
        """
        result = delete_schedule(schedule_id)
        return result, 200
