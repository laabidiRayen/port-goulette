# services/port_facility_service.py

from models.port_facility import PortFacility  # Assuming a model for port facilities
from extensions import db

# Get all port facilities (like parking, lounge, etc.)
def get_all_port_facilities():
    return PortFacility.query.all()

# Get a specific port facility by ID (e.g., parking space or lounge)
def get_port_facility_by_id(id):
    return PortFacility.query.get(id)

# Add a new port facility
def add_port_facility(name, description, operational_hours):
    facility = PortFacility(name=name, description=description, operational_hours=operational_hours)
    db.session.add(facility)
    db.session.commit()
    return facility

# Update a port facility
def update_port_facility(id, name, description, operational_hours):
    facility = PortFacility.query.get(id)
    if facility:
        facility.name = name
        facility.description = description
        facility.operational_hours = operational_hours
        db.session.commit()
        return facility
    return None