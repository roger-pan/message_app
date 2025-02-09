from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from .config import ProductionConfig, DevelopmentConfig

db = SQLAlchemy()

def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)

    login = LoginManager(app)
    login.login_view = 'url to login...'

    app.config.from_object(DevelopmentConfig)
    db.init_app(app)

    with app.app_context():

        # Imports
        from . import routes

        # Create tables for our models
        db.create_all()

        return app