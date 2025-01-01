# services/schedule_service.py

from models.schedule import Schedule
from extensions import db

# Get all schedules
def get_all_schedules():
    return Schedule.query.all()

# Get a specific schedule by ID
def get_schedule_by_id(id):
    return Schedule.query.get(id)

# Add a new schedule
def add_schedule(ship_id, arrival_time, departure_time):
    schedule = Schedule(ship_id=ship_id, arrival_time=arrival_time, departure_time=departure_time)
    db.session.add(schedule)
    db.session.commit()
    return schedule

# Update an existing schedule
def update_schedule(id, arrival_time, departure_time):
    schedule = Schedule.query.get(id)
    if schedule:
        schedule.arrival_time = arrival_time
        schedule.departure_time = departure_time
        db.session.commit()
        return schedule
    return None

# Delete a schedule by ID
def delete_schedule(id):
    schedule = Schedule.query.get(id)
    if schedule:
        db.session.delete(schedule)
        db.session.commit()
        return {'message': 'Schedule deleted successfully'}
    return {'error': 'Schedule not found'}, 404
