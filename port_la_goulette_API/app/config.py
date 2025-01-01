#This file manages configuration settings for your application, such as database URLs, API keys, or debug flags.

# import os

# # config.py
# class Config:
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  # SQLite file named app.db
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

import os

# config.py
class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'  # SQLite file named app.db
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Swagger Configuration
    API_TITLE = "La Goulette Port Management API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
