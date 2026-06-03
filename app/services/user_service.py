"""
app/services/user_service.py
─────────────────────────────
Business logic for user registration, lookup, and updates.
Keeps route handlers thin.
"""
from datetime import datetime, timezone
from typing import Optional

from flask import current_app
from sqlalchemy.exc import IntegrityError

from app import db
from app.models.user import User, VALID_ROLES, ROLE_STUDENT


class UserExistsError(Exception):
    """Raised when trying to register an email that already exists."""


class InvalidRoleError(Exception):
    """Raised when an invalid role is provided."""


def register_user(
    first_name: str,
    last_name: str,
    email: str,
    password: str,
    role: str = ROLE_STUDENT,
) -> User:
    """
    Create and persist a new user.
    Raises UserExistsError if the email is already taken.
    Raises InvalidRoleError for unrecognised roles.
    """
    if role not in VALID_ROLES:
        raise InvalidRoleError(f"Invalid role: {role!r}")

    user = User(
        first_name=first_name.strip(),
        last_name=last_name.strip(),
        email=email.strip().lower(),
        role=role,
    )
    user.set_password(password)

    db.session.add(user)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        raise UserExistsError(f"Email already registered: {email}")

    current_app.logger.info("New user registered: %s (%s)", user.email, user.role)
    return user


def get_user_by_email(email: str) -> Optional[User]:
    return User.query.filter_by(email=email.strip().lower()).first()


def get_user_by_id(user_id: int) -> Optional[User]:
    return db.session.get(User, user_id)


def authenticate(email: str, password: str) -> Optional[User]:
    """Return user if credentials are valid and account is active, else None."""
    user = get_user_by_email(email)
    if user and user.is_active and user.check_password(password):
        user.record_login()
        return user
    return None


def all_users(page: int = 1, per_page: int = 20):
    """Paginated list of all users for admin views."""
    return User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
