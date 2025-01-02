from datetime import datetime
from extensions import db
from .relationships import ship_service_association
class Ship(db.Model):
    __tablename__ = 'ships'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)  # e.g., Cargo, Passenger
    arrival_time = db.Column(db.DateTime, nullable=False)
    departure_time = db.Column(db.DateTime)
    status = db.Column(db.String(50), nullable=False, default="arrived")  # status field (e.g., "arrived", "departed", "docked")

    # Many-to-Many Relationship with Service
    services = db.relationship('Service', secondary=ship_service_association, back_populates='ships')