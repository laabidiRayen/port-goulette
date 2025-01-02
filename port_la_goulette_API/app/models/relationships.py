# relationships.py
from extensions import db

ship_service_association = db.Table(
    'ship_service',
    db.Column('ship_id', db.Integer, db.ForeignKey('ships.id'), primary_key=True),
    db.Column('service_id', db.Integer, db.ForeignKey('services.id'), primary_key=True)
)