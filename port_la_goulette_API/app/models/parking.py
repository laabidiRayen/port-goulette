from extensions import db

class Parking(db.Model):
    __tablename__ = 'parkings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)
    price_per_hour = db.Column(db.Float, nullable=False)
