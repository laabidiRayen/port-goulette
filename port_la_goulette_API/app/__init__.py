from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.extensions import db,migrate,mail
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
    mail.init_app(app)

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
