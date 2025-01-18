from flask import Flask
from extensions import db, migrate, api, mail, jwt
from ressources.user_route import blp as user_blp
from ressources.schedule_route import blp as schedule_blp
from ressources.booking_route import blp as booking_blp
from ressources.feedback_route import blp as feedback_blp
from ressources.port_facility_route import blp as port_facility_blp
from ressources.parking_route import blp as parking_blp
from ressources.ship_route import blp as ship_blp
from ressources.service_route import blp as service_blp

def create_app():
    app = Flask(__name__)

    # Load configurations
    app.config.from_object('config.Config')

    # Initialize the API (Flask-Smorest)
    api.init_app(app)

    # Register blueprints (resources)
    api.register_blueprint(user_blp)
    api.register_blueprint(schedule_blp)
    api.register_blueprint(booking_blp)
    api.register_blueprint(feedback_blp)
    api.register_blueprint(port_facility_blp)
    api.register_blueprint(parking_blp)
    api.register_blueprint(ship_blp)
    api.register_blueprint(service_blp)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    jwt.init_app(app)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
