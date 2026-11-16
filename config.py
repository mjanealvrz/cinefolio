
import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "reeltrack-dev-secret-key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///reeltrack.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
