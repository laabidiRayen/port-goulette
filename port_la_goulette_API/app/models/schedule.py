from extensions import db

class Schedule(db.Model):
    __tablename__ = 'schedules'
    id = db.Column(db.Integer, primary_key=True)
    ship_id = db.Column(db.Integer, db.ForeignKey('ships.id'), nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)

    # Relationships
    ship = db.relationship('Ship', backref='schedules')