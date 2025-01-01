from extensions import db

class PortFacility(db.Model):
    __tablename__ = 'port_facilities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    operational_hours = db.Column(db.String(50), nullable=True)
