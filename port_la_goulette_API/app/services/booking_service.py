
from models import Booking,relationships
from models.relationships import ship_service_association
from datetime import datetime
from extensions import db

# Create a new booking
def create_booking(data):
    try:
        user_id = data.get('user_id')
        service_id = data.get('service_id')
        booking_date = data.get('booking_date')

        # If no booking_date is provided, set it to the current time
        if not booking_date:
            booking_date = datetime.now()
        else:
            # Ensure booking_date is a string, then parse it to a datetime object
            booking_date = datetime.fromisoformat(booking_date) if isinstance(booking_date, str) else datetime.now()

        # Create a new booking object
        booking = Booking(
            user_id=user_id,
            service_id=service_id,
            booking_date=booking_date
        )
        
        # Add to the database
        db.session.add(booking)
        db.session.commit()

        return booking

    except Exception as e:
        raise ValueError(f"Error creating booking: {str(e)}")

# Get all bookings
def get_all_bookings():
    return Booking.query.all()

# Get bookings for a specific ship
def get_bookings_for_ship(ship_id):
    return Booking.query.join(ship_service_association, ship_service_association.c.service_id == Booking.service_id) \
                         .filter(ship_service_association.c.ship_id == ship_id) \
                         .all()

# Get bookings for a specific service
def get_bookings_for_service(service_id):
    return Booking.query.filter_by(service_id=service_id).all()

# Cancel a booking by ID
def cancel_booking(booking_id):
    booking = Booking.query.get(booking_id)
    if booking:
        db.session.delete(booking)
        db.session.commit()
        return True
    return False
