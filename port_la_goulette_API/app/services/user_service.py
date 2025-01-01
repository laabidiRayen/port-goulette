# services/user_service.py
from models.user import User
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

# Register a new user
def register_user(username, email, password):
    hashed_password = generate_password_hash(password)
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return user

# Authenticate a user
def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        return user
    return None
# Update user details
def update_user(id, username, email):
    user = User.query.get(id)
    if not user:
        return None  # User not found

    # Check for duplicate email in the database
    existing_user = User.query.filter(User.email == email, User.id != id).first()
    if existing_user:
        raise IntegrityError(None, None, "Email is already in use")  # Email conflict

    user.username = username
    user.email = email
    db.session.commit()
    return user

# Delete a user
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return None  # User not found

    db.session.delete(user)
    db.session.commit()
    return True
