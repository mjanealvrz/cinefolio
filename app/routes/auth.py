
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from app import db
from app.models import User
from app.forms import RegisterForm, LoginForm


# Create authentication Blueprint
auth = Blueprint("auth", __name__)


# REGISTRATION ROUTE
@auth.route("/register", methods=["GET", "POST"])
def register():

    # Redirect if the user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = RegisterForm()

    if form.validate_on_submit():

        # Check if username or email already exists
        existing_user = User.query.filter(
            (User.username == form.username.data) |
            (User.email == form.email.data)
        ).first()

        if existing_user:
            flash("Username or email already exists.", "danger")
            return render_template("register.html", form=form)

        # Create a new user
        user = User(
            username=form.username.data,
            email=form.email.data
        )

        # Hash the password before saving
        user.set_password(form.password.data)

        # Save the new user to the database
        db.session.add(user)
        db.session.commit()

        flash(
            "Your account has been created! You can now log in.",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template("register.html", form=form)


# LOGIN ROUTE
@auth.route("/login", methods=["GET", "POST"])
def login():

    # Redirect if the user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()

    if form.validate_on_submit():

        # Find the user using their email
        user = User.query.filter_by(
            email=form.email.data
        ).first()

        # Check if the account exists and password is correct
        if user and user.check_password(form.password.data):

            login_user(user)

            flash("Welcome back to CineFolio!", "success")

            return redirect(url_for("main.dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html", form=form)


# LOGOUT ROUTE
@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash("You have been logged out.", "info")

    return redirect(url_for("auth.login"))
