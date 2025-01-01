from flask_smorest import Blueprint
from flask.views import MethodView
from flask import jsonify
from schemas import UserRegisterSchema, UserLoginSchema, UserUpdateSchema
from services.user_service import register_user, authenticate_user, update_user, delete_user
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, NotFound

blp = Blueprint("Users", "users", url_prefix="/users", description="Operations related to users")

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)  # Use the UserRegisterSchema here
    @blp.response(201, description="User registered successfully")
    @blp.response(400, description="Email is already in use")  # Client error for duplicates
    @blp.response(500, description="Internal server error")  # Unexpected issues
    def post(self, data):
        try:
            username = data["username"]
            email = data["email"]
            password = data["password"]
            new_user = register_user(username, email, password)
            return {"message": f"User {new_user.username} registered successfully"}, 201
        except IntegrityError as e:
            if "email" in str(e.orig):
                response = jsonify({"message": "Email is already in use"})
                response.status_code = 400
                return response
            response = jsonify({"message": "A conflict occurred during registration"})
            response.status_code = 400
            return response
        except Exception as e:
            response = jsonify({"message": "An unexpected error occurred"})
            response.status_code = 500
            return response

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)  # Use the UserLoginSchema here
    @blp.response(200, description="Login successful")
    @blp.response(401, description="Invalid username or password")
    def post(self, data):
        try:
            username = data["username"]
            password = data["password"]
            user = authenticate_user(username, password)
            if user:
                return {"message": f"Welcome {user.username}"}, 200
            response = jsonify({"message": "Invalid username or password"})
            response.status_code = 401
            return response
        except Exception as e:
            response = jsonify({"message": f"An unexpected error occurred: {str(e)}"})
            response.status_code = 500
            return response




@blp.route("/update/<int:user_id>")
class UserUpdate(MethodView):
    @blp.arguments(UserUpdateSchema)  # Use the UserUpdateSchema here
    @blp.response(200, description="User updated successfully")
    @blp.response(404, description="User not found")
    @blp.response(400, description="Invalid input data")
    @blp.response(409, description="Email already in use")  # Conflict for duplicate email
    def put(self, data, user_id):
        try:
            username = data["username"]
            email = data["email"]
            updated_user = update_user(user_id, username, email)
            if updated_user:
                return {"message": f"User {updated_user.username} updated successfully"}, 200
            response = jsonify({"message": "User not found"})
            response.status_code = 404
            return response
        except IntegrityError as e:
            if "email" in str(e.orig):
                response = jsonify({"message": "Email is already in use"})
                response.status_code = 409  # Conflict error
                return response
            response = jsonify({"message": "credential already taken"})
            response.status_code = 400
            return response
        except BadRequest as e:
            response = jsonify({"message": str(e)})
            response.status_code = 400
            return response
        except Exception as e:
            response = jsonify({"message": f"An unexpected error occurred: {str(e)}"})
            response.status_code = 500
            return response




@blp.route("/delete/<int:user_id>")
class UserDelete(MethodView):
    @blp.response(200, description="User deleted successfully")
    @blp.response(404, description="User not found")
    def delete(self, user_id):
        try:
            result = delete_user(user_id)
            if result:
                return {"message": f"User with ID {user_id} deleted successfully"}, 200
            response = jsonify({"message": "User not found"})
            response.status_code = 404
            return response
        except Exception as e:
            response = jsonify({"message": f"An unexpected error occurred: {str(e)}"})
            response.status_code = 500
            return response