#This file centralizes the setup of third-party Flask extensions to avoid repetitive code in main.py
#Purpose:
#Configure and initialize extensions like SQLAlchemy, JWT, or others.


from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from flask_mail import Mail

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
mail = Mail()
api = Api()
