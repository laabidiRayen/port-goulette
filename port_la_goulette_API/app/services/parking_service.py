from models.parking import Parking
from extensions import db


def get_all_parking_spaces():
    """Retrieve all parking spaces."""
    return Parking.query.all()


def get_parking_by_id(parking_id):
    """Retrieve a parking space by ID."""
    return Parking.query.get(parking_id)


def create_parking_space(data):
    """Create a new parking space."""
    parking = Parking(**data)
    db.session.add(parking)
    db.session.commit()
    return parking


def update_parking_space(parking_id, data):
    """Update an existing parking space."""
    parking = Parking.query.get(parking_id)
    if not parking:
        return None
    for key, value in data.items():
        setattr(parking, key, value)
    db.session.commit()
    return parking


def delete_parking_space(parking_id):
    """Delete a parking space."""
    parking = Parking.query.get(parking_id)
    if parking:
        db.session.delete(parking)
        db.session.commit()
        return True
    return False


def book_parking_space(parking_id, user_id):
    """Book a parking space."""
    parking = Parking.query.get(parking_id)
    if not parking or parking.available_slots <= 0:
        return None
    parking.available_slots -= 1
    db.session.commit()
    return parking
