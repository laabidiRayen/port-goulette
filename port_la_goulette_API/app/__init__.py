# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from app.routes import booking_route, schedule_route, user_route
# from flask_jwt_extended import JWTManager
# from flask_mail import Mail
# from flask_cors import CORS

# db = SQLAlchemy()
# jwt = JWTManager()
# mail = Mail()

# def create_app():
#     app = Flask(__name__)
    
#     # Configuration
#     app.config.from_object('app.config.Config')
    
#     # Initialize extensions
#     db.init_app(app)
#     jwt.init_app(app)
#     mail.init_app(app)
#     CORS(app)
    
#     # Register routes
#     from app.routes import feedback
#     app.register_blueprint(user_route.bp)
#     app.register_blueprint(schedule_route.bp)
#     app.register_blueprint(booking_route.bp)
#     app.register_blueprint(feedback.bp)
    
#     return app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.extensions import db,migrate
from flask_migrate import Migrate
from .config import Config  # Configuration settings (create this file if not exists)

# Create a function to initialize the Flask app
def create_app():
    # Initialize Flask app
    app = Flask(__name__)

    # Load the configuration from the Config class
    app.config.from_object(Config)

    # Initialize the extensions with the app
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints (routes)
    from app.ressources.user_route import blp as user_blp
    from app.ressources.schedule_route import blp as schedule_blp
    from app.ressources.booking_route import blp as booking_blp
    from app.ressources.feedback_route import blp as feedback_blp
    from app.ressources.port_facility_route import blp as port_facility_blp
    from app.ressources.parking_route import blp as parking_blp
    from app.ressources.ship_route import blp as ship_blp
    from app.ressources.service_route import blp as service_blp


    app.register_blueprint(user_blp)
    app.register_blueprint(schedule_blp)
    app.register_blueprint(booking_blp)
    app.register_blueprint(feedback_blp)
    app.register_blueprint(port_facility_blp)
    app.register_blueprint(parking_blp)
    app.register_blueprint(ship_blp)
    app.register_blueprint(service_blp)

    return app
