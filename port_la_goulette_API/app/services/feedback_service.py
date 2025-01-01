# services/feedback_service.py

from models.feedback import Feedback
from extensions import db

# Add feedback for a service or ship
def add_feedback(user_id, service_id, feedback_text):
    feedback = Feedback(user_id=user_id, service_id=service_id, feedback_text=feedback_text)
    db.session.add(feedback)
    db.session.commit()
    return feedback

# Get all feedback for a service or ship
def get_all_feedback():
    return Feedback.query.all()

# Get feedback for a specific service
def get_feedback_for_service(service_id):
    return Feedback.query.filter_by(service_id=service_id).all()

# Delete feedback
def delete_feedback(id):
    feedback = Feedback.query.get(id)
    if feedback:
        db.session.delete(feedback)
        db.session.commit()
        return {'message': 'Feedback deleted successfully'}
    return {'error': 'Feedback not found'}, 404
