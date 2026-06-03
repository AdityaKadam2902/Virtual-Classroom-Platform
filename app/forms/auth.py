"""
app/forms/auth.py
─────────────────
WTForms for registration and login.
Server-side validation keeps business logic out of route handlers.
"""
from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import (
    DataRequired, Email, EqualTo, Length, ValidationError
)

from app.models.user import ROLE_STUDENT, ROLE_INSTRUCTOR


class RegistrationForm(FlaskForm):
    first_name = StringField(
        "First Name",
        validators=[DataRequired(), Length(min=2, max=64)],
    )
    last_name = StringField(
        "Last Name",
        validators=[DataRequired(), Length(min=2, max=64)],
    )
    email = EmailField(
        "Email Address",
        validators=[DataRequired(), Email(), Length(max=120)],
    )
    role = SelectField(
        "I am joining as",
        choices=[
            (ROLE_STUDENT, "Student – I want to learn"),
            (ROLE_INSTRUCTOR, "Instructor – I want to teach"),
        ],
        default=ROLE_STUDENT,
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=8, max=128)],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")],
    )
    terms = BooleanField(
        "I agree to the Terms and Conditions",
        validators=[DataRequired(message="You must accept the terms.")],
    )
    submit = SubmitField("Create Account")

    def validate_password(self, field):
        """Enforce basic password complexity."""
        pw = field.data or ""
        if not any(c.isupper() for c in pw):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not any(c.isdigit() for c in pw):
            raise ValidationError("Password must contain at least one digit.")


class LoginForm(FlaskForm):
    email = EmailField(
        "Email Address",
        validators=[DataRequired(), Email()],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
    )
    remember = BooleanField("Remember me")
    submit = SubmitField("Sign In")
