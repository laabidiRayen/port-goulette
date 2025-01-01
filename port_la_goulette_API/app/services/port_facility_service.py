# services/port_facility_service.py

from models.port_facility import PortFacility  # Assuming a model for port facilities
from extensions import db

# Get all port facilities (like parking, lounge, etc.)
def get_all_port_facilities():
    return PortFacility.query.all()

# Get a specific port facility by ID (e.g., parking space or lounge)
def get_port_facility_by_id(id):
    return PortFacility.query.get(id)

# Add a new port facility (e.g., new parking spot)
def add_port_facility(name, type, capacity):
    facility = PortFacility(name=name, type=type, capacity=capacity)
    db.session.add(facility)
    db.session.commit()
    return facility

# Update a port facility (e.g., parking spot capacity)
def update_port_facility(id, name, type, capacity):
    facility = PortFacility.query.get(id)
    if facility:
        facility.name = name
        facility.type = type
        facility.capacity = capacity
        db.session.commit()
        return facility
    return None
