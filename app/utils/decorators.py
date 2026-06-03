"""
app/utils/decorators.py
────────────────────────
Reusable route decorators for role-based access control.
"""
from functools import wraps

from flask import abort
from flask_login import current_user


def instructor_required(f):
    """Allow access only to instructors and admins."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_instructor:
            abort(403)
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    """Allow access only to admins."""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated
