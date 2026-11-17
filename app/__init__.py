
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config


# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()


# Configure Flask-Login
login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"


@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return db.session.get(User, int(user_id))


# Application factory
def create_app():

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)

    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Import and register blueprints ONCE
    from app.routes import main
    from app.routes.auth import auth

    app.register_blueprint(main)
    app.register_blueprint(auth)

    # Create database tables
    with app.app_context():
        from app import models
        db.create_all()

    return app
