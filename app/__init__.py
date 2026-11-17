
import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# Initialize SQLAlchemy first
db = SQLAlchemy()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)

    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize database
    db.init_app(app)

    # Register routes
    from app.routes import main
    app.register_blueprint(main)

    # Register models and create tables
    with app.app_context():
        from app import models  # pyright: ignore[reportUnusedImport]
        db.create_all()

    return app
