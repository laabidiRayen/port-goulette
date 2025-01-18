from flask_smorest import Blueprint
from flask.views import MethodView
from flask import jsonify,request, current_app
from schemas import UserRegisterSchema, UserLoginSchema, UserUpdateSchema
from services.user_service import register_user, authenticate_user, update_user, delete_user
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import BadRequest, NotFound
import jwt
from functools import wraps
import datetime
from models.user import User
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
# authorizations = {
#     'jsonWebToken': {
#         'type': 'apiKey',
#         'in': 'header',
#         'name':'Authorization'}
# }

blp = Blueprint("Users", "users", url_prefix="/users", description="Operations related to users")


# Verify token
# def token_required(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = request.headers.get('Authorization')
#         if not token:
#             return jsonify({'message': "Token is missing"}), 403
#         try:
#             data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
#             current_user = User.query.filter_by(id=data['user']).first()
#         except jwt.ExpiredSignatureError:
#             return jsonify({'message': "Expired token"}), 403
#         except jwt.InvalidTokenError:
#             return jsonify({'message': "Invalid token"}), 403
#         return f(current_user, *args, **kwargs)
#     return decorated


@blp.route("/users")
class UserList(MethodView):
    @blp.response(200, description="List of all users")
    def get(self):
        users = User.query.all()
        return jsonify([{"id": user.id, "username": user.username, "email": user.email} for user in users])


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
            token = create_access_token(identity=new_user.id)
            return {"message": f"User {new_user.username} registered successfully", "token": token}, 201
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

@blp.route("/jwt-login")
class UserJWTLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    @blp.response(200, description="Login successful")
    @blp.response(401, description="Invalid username or password")
    def post(self, data):
        try:
            username = data["username"]
            password = data["password"]
            user = authenticate_user(username, password)
            if user:
                # token = jwt.encode({'user': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, current_app.config["SECRET_KEY"])
                token = create_access_token(identity=user.id)
                return {"message": f"Welcome {user.username}", "token": token}, 200
            response = jsonify({"message": "Invalid username or password"})
            response.status_code = 401
            return response
        except Exception as e:
            response = jsonify({"message": f"An unexpected error occurred: {str(e)}"})
            response.status_code = 500
            return response



@blp.route("/update/<int:user_id>")
class UserUpdate(MethodView):
    # @jwt_required()
    # @blp.doc(security=[{"jsonWebToken": []}])
    @blp.arguments(UserUpdateSchema)  # Use the UserUpdateSchema here
    @blp.response(200, description="User updated successfully")
    @blp.response(404, description="User not found")
    @blp.response(400, description="Invalid input data")
    @blp.response(409, description="Email already in use")  # Conflict for duplicate email
    
    def put(self, data, user_id):
        # current_user_id = get_jwt_identity()
        # if current_user_id != user_id:
        #     return jsonify({"message": "Unauthorized"}), 403
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
    # @jwt_required()
    @blp.response(200, description="User deleted successfully")
    @blp.response(404, description="User not found")
    # @blp.doc(security=[{"jsonWebToken": []}])
    def delete(self, user_id):
        # current_user_id = get_jwt_identity()
        # if current_user_id != user_id:
        #     return jsonify({"message": "Unauthorized"}), 403
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