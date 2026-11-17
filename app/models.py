
from datetime import datetime, timezone

from werkzeug.security import generate_password_hash, check_password_hash
from app import db


# USER TABLE
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    watchlist_items = db.relationship(
        "WatchlistItem",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    reviews = db.relationship(
        "Review",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# MEDIA TABLE
class Media(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(200), nullable=False)
    media_type = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text)
    poster_path = db.Column(db.String(300))
    release_year = db.Column(db.Integer)

    watchlist_items = db.relationship(
        "WatchlistItem",
        back_populates="media",
        cascade="all, delete-orphan"
    )

    reviews = db.relationship(
        "Review",
        back_populates="media",
        cascade="all, delete-orphan"
    )


# WATCHLIST TABLE
class WatchlistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    media_id = db.Column(
        db.Integer,
        db.ForeignKey("media.id"),
        nullable=False
    )

    status = db.Column(db.String(30), default="Plan to Watch")

    added_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    user = db.relationship("User", back_populates="watchlist_items")
    media = db.relationship("Media", back_populates="watchlist_items")

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "media_id",
            name="unique_user_media"
        ),
    )


# REVIEW TABLE
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    media_id = db.Column(
        db.Integer,
        db.ForeignKey("media.id"),
        nullable=False
    )

    rating = db.Column(db.Integer, nullable=False)
    review_text = db.Column(db.Text)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc)
    )

    user = db.relationship("User", back_populates="reviews")
    media = db.relationship("Media", back_populates="reviews")
