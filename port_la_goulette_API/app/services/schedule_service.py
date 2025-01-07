# services/schedule_service.py

from models.booking import Booking
from models.service import Service
from models.schedule import Schedule
from models.ship import Ship
from models.relationships import ship_service_association
from extensions import db
from utils.notifications import send_email

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
    changes = []
    if schedule.arrival_time != arrival_time:
        changes.append(f"Arrival time updated from {schedule.arrival_time} to {arrival_time}")
    if schedule.departure_time != departure_time:
        changes.append(f"Departure time updated from {schedule.departure_time} to {departure_time}")
    if ship_id and schedule.ship_id != ship_id:
        changes.append(f"Ship updated from {schedule.ship_id} to {ship_id}")

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

    if changes:
        # Fetch the list of users waiting for updates on this schedule
        services = db.session.query(Service).join(ship_service_association).filter(ship_service_association.c.ship_id == ship_id).all()
        # Find users who have booked those services
        user_emails = set()
        for service in services:
            bookings = Booking.query.filter_by(service_id=service.id).all()
            for booking in bookings:
                user_emails.add(booking.user.email)

        # Send notification emails
        for email in user_emails:
            send_email(email, "Schedule Updated", changes)
    

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