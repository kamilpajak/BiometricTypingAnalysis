# auth_routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, session
from sqlalchemy.exc import IntegrityError

from database import db
from forms import LoginForm, RegistrationForm
from models.user import User

auth_bp = Blueprint("auth", __name__, template_folder="templates")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("Email already registered. Please log in.", "danger")
            return redirect(url_for("auth.login"))
        if User.query.filter_by(username=form.username.data).first():
            flash("Username already taken. Please choose a different one.", "danger")
            return redirect(url_for("auth.register"))
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        try:
            db.session.commit()
            flash("Account created successfully! You can now log in.", "success")
            return redirect(url_for("auth.login"))
        except IntegrityError:
            db.session.rollback()
            flash(
                "There was an issue creating the account. Please try again.", "danger"
            )
            return redirect(url_for("auth.register"))
    return render_template("register.html", title="Register", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session["user_id"] = user.id
            flash("You have been logged in!", "success")
            return redirect(url_for("capture.index"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", title="Login", form=form)


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("auth.login"))
