# ressources/feedback.py

from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from services.feedback_service import (
    add_feedback,
    get_all_feedback,
    get_feedback_for_service,
    delete_feedback
)

blp = Blueprint("Feedbacks", "feedbacks", url_prefix="/feedbacks", description="Operations related to feedback")

@blp.route("/")
class FeedbackList(MethodView):
    @blp.response(200, description="List of all feedbacks")
    def get(self):
        """
        Retrieve all feedbacks.
        """
        feedbacks = get_all_feedback()
        return [feedback.to_dict() for feedback in feedbacks], 200

    @blp.arguments(schema=None)  # Replace with proper schema if used
    @blp.response(201, description="Feedback added successfully")
    @blp.response(400, description="Invalid data provided")
    def post(self):
        """
        Add new feedback for a service or ship.
        """
        data = request.get_json()
        user_id = data.get('user_id')
        service_id = data.get('service_id')
        feedback_text = data.get('feedback_text')

        if not user_id or not service_id or not feedback_text:
            return {"error": "Missing required fields"}, 400

        feedback = add_feedback(user_id, service_id, feedback_text)
        return {"message": "Feedback added successfully", "feedback": feedback.to_dict()}, 201


@blp.route("/service/<int:service_id>")
class FeedbackForService(MethodView):
    @blp.response(200, description="List of feedback for a specific service")
    def get(self, service_id):
        """
        Retrieve all feedback for a specific service.
        """
        feedbacks = get_feedback_for_service(service_id)
        return [feedback.to_dict() for feedback in feedbacks], 200


@blp.route("/<int:feedback_id>")
class FeedbackDetail(MethodView):
    @blp.response(200, description="Feedback deleted successfully")
    @blp.response(404, description="Feedback not found")
    def delete(self, feedback_id):
        """
        Delete a feedback by ID.
        """
        result = delete_feedback(feedback_id)
        if result:
            return {"message": "Feedback deleted successfully"}, 200
        return {"message": "Feedback not found"}, 404
