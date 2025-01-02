
from extensions import db
from models.feedback import Feedback

def get_all_feedback():
    try:
        return Feedback.query.all()
    except Exception as e:
        raise RuntimeError(f"Failed to retrieve feedbacks: {str(e)}")

def add_feedback(user_id, message, rating=None):
    try:
        feedback = Feedback(user_id=user_id, message=message, rating=rating)
        db.session.add(feedback)
        db.session.commit()
        return feedback
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Failed to add feedback: {str(e)}")

def delete_feedback(feedback_id):
    try:
        feedback = Feedback.query.get(feedback_id)
        if not feedback:
            return False
        db.session.delete(feedback)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        raise RuntimeError(f"Failed to delete feedback: {str(e)}")
