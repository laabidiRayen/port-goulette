from extensions import db
from .relationships import ship_service_association
class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    # Many-to-Many Relationship with Ship
    ships = db.relationship('Ship', secondary=ship_service_association, back_populates='services')