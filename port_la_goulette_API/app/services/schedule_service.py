# services/schedule_service.py

from models.schedule import Schedule
from models.ship import Ship
from extensions import db

# Get all schedules
def get_all_schedules():
    return Schedule.query.all()

# Get a specific schedule by ID
def get_schedule_by_id(id):
    return Schedule.query.get(id)

# Add a new schedule
def add_schedule(ship_id, arrival_time, departure_time):
    """
    Add a new schedule.
    """
    # Check if the ship_id exists in the ships table
    ship = Ship.query.get(ship_id)
    if not ship:
        raise ValueError(f"Ship with ID {ship_id} does not exist.")

    # Create the new schedule
    schedule = Schedule(
        ship_id=ship_id,
        arrival_time=arrival_time,
        departure_time=departure_time
    )
    db.session.add(schedule)
    db.session.commit()
    return schedule

# Update an existing schedule
def update_schedule(schedule_id, arrival_time, departure_time, ship_id=None):
    schedule = Schedule.query.get(schedule_id)
    if not schedule:
        raise ValueError("Schedule not found")

    # Update the schedule details
    schedule.arrival_time = arrival_time
    schedule.departure_time = departure_time

    # Update the ship_id if provided
    if ship_id:
        ship = Ship.query.get(ship_id)
        if not ship:
            raise ValueError("Invalid ship_id, no such ship exists.")
        schedule.ship_id = ship_id  # Update the relationship

    db.session.commit()
    return schedule

# Delete a schedule by ID
def delete_schedule(id):
    schedule = Schedule.query.get(id)
    if schedule:
        db.session.delete(schedule)
        db.session.commit()
        return {'message': 'Schedule deleted successfully'}
    return {'error': 'Schedule not found'}, 404

def get_schedules_by_ship_id(ship_id):
    """
    Retrieve all schedules for a specific ship by ship_id.
    """
    return Schedule.query.filter_by(ship_id=ship_id).all()