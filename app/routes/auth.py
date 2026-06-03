"""
app/routes/auth.py
──────────────────
Authentication routes: register, login, logout.
"""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.forms.auth import LoginForm, RegistrationForm
from app.services.user_service import UserExistsError, authenticate, register_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = RegistrationForm()
    if form.validate_on_submit():
        try:
            user = register_user(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=form.password.data,
                role=form.role.data,
            )
            login_user(user, remember=False)
            flash("Welcome to LearnHub! Your account has been created.", "success")
            return redirect(url_for("dashboard.index"))
        except UserExistsError:
            flash("That email is already registered. Please log in.", "warning")

    return render_template("auth/register.html", form=form)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = authenticate(form.email.data, form.password.data)
        if user:
            login_user(user, remember=form.remember.data)
            flash(f"Welcome back, {user.first_name}!", "success")
            # Honour the ?next= redirect safely
            next_page = request.args.get("next")
            if next_page and next_page.startswith("/"):
                return redirect(next_page)
            return redirect(url_for("dashboard.index"))
        flash("Invalid email or password. Please try again.", "danger")

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been signed out.", "info")
    return redirect(url_for("main.home"))
