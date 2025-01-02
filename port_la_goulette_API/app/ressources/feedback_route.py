# ressources/feedback.py

from flask_smorest import Blueprint
from flask.views import MethodView
from flask import request
from services.feedback_service import (
    add_feedback,
    get_all_feedback,
    delete_feedback
)
from schemas import FeedbackSchema  # Importing the schema

blp = Blueprint("Feedbacks", "feedbacks", url_prefix="/feedbacks", description="Operations related to feedback")

@blp.route("/")
class FeedbackList(MethodView):
    @blp.response(200, FeedbackSchema(many=True), description="List of all feedbacks")
    def get(self):
        """
        Retrieve all feedbacks.
        """
        feedbacks = get_all_feedback()
        return feedbacks  

    @blp.arguments(FeedbackSchema)
    @blp.response(201, FeedbackSchema, description="Feedback added successfully")
    @blp.response(400, description="Invalid data provided")
    def post(self, data):
        """
        Add new feedback.
        """
        feedback = add_feedback(
            user_id=data["user_id"],
            message=data["message"],
            rating=data.get("rating"),
        )
        return FeedbackSchema().dump(feedback),201


@blp.route("/<int:feedback_id>")
class FeedbackDetail(MethodView):
    @blp.response(200, FeedbackSchema, description="Feedback deleted successfully")
    @blp.response(404, description="Feedback not found")
    def delete(self, feedback_id):
        """
        Delete a feedback by ID.
        """
        result = delete_feedback(feedback_id)
        if result:
            return {"message": "Feedback deleted successfully"}, 200
        return {"message": "Feedback not found"}, 404
