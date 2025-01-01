from extensions import db

class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    booking_date = db.Column(db.DateTime, default=db.func.now(), nullable=False)

    # Relationships
    user = db.relationship('User', backref='bookings')
    service = db.relationship('Service', backref='bookings')
