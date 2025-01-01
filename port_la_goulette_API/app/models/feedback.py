from extensions import db

class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=True)  # Optional: Rating out of 5
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
