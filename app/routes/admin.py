"""
app/routes/admin.py
────────────────────
Admin-only management panel: users, courses overview.
"""
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.models.course import Category, Course
from app.models.user import User
from app.services.course_service import all_categories, get_or_create_category
from app.utils.decorators import admin_required

admin_bp = Blueprint("admin", __name__)


# ── Guard: all admin routes require admin role ────────────────────────────────

@admin_bp.before_request
@login_required
def check_admin():
    if not current_user.is_admin:
        abort(403)


# ── Overview ─────────────────────────────────────────────────────────────────

@admin_bp.route("/")
def index():
    user_count = User.query.count()
    course_count = Course.query.count()
    published_count = Course.query.filter_by(is_published=True).count()
    categories = all_categories()
    return render_template(
        "admin/index.html",
        user_count=user_count,
        course_count=course_count,
        published_count=published_count,
        categories=categories,
    )


# ── Users ─────────────────────────────────────────────────────────────────────

@admin_bp.route("/users")
def users():
    page = request.args.get("page", 1, type=int)
    users_page = User.query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template("admin/users.html", users=users_page)


@admin_bp.route("/users/<int:user_id>/toggle-active", methods=["POST"])
def toggle_user_active(user_id: int):
    user = db.session.get(User, user_id)
    if not user:
        abort(404)
    if user.id == current_user.id:
        flash("You cannot deactivate your own account.", "warning")
        return redirect(url_for("admin.users"))
    user.is_active = not user.is_active
    db.session.commit()
    state = "activated" if user.is_active else "deactivated"
    flash(f"User {user.email} has been {state}.", "success")
    return redirect(url_for("admin.users"))


# ── Courses ───────────────────────────────────────────────────────────────────

@admin_bp.route("/courses")
def courses():
    page = request.args.get("page", 1, type=int)
    courses_page = Course.query.order_by(Course.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template("admin/courses.html", courses=courses_page)


@admin_bp.route("/courses/<int:course_id>/toggle-publish", methods=["POST"])
def toggle_publish(course_id: int):
    course = db.session.get(Course, course_id)
    if not course:
        abort(404)
    course.is_published = not course.is_published
    db.session.commit()
    state = "published" if course.is_published else "unpublished"
    flash(f"Course «{course.title}» has been {state}.", "success")
    return redirect(url_for("admin.courses"))


# ── Categories ────────────────────────────────────────────────────────────────

@admin_bp.route("/categories", methods=["GET", "POST"])
def categories():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        if name:
            cat = get_or_create_category(name)
            flash(f"Category «{cat.name}» ready.", "success")
        return redirect(url_for("admin.categories"))

    cats = all_categories()
    return render_template("admin/categories.html", categories=cats)
