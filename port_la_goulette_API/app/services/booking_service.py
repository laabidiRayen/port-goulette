# services/booking_service.py

from models.booking import Booking
from extensions import db

# Create a new booking for a ship or service
def create_booking(ship_id, service_id, user_id, date_time):
    booking = Booking(ship_id=ship_id, service_id=service_id, user_id=user_id, date_time=date_time)
    db.session.add(booking)
    db.session.commit()
    return booking

# Get all bookings for a specific ship
def get_bookings_for_ship(ship_id):
    return Booking.query.filter_by(ship_id=ship_id).all()

# Get all bookings for a specific service
def get_bookings_for_service(service_id):
    return Booking.query.filter_by(service_id=service_id).all()

# Cancel a booking by ID
def cancel_booking(id):
    booking = Booking.query.get(id)
    if booking:
        db.session.delete(booking)
        db.session.commit()
        return {'message': 'Booking canceled successfully'}
    return {'error': 'Booking not found'}, 404
