"""
app/routes/main.py
──────────────────
Public pages: home, about.
"""
from flask import Blueprint, render_template

from app.models.course import Category, Course

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():
    featured = (
        Course.query
        .filter_by(is_published=True)
        .order_by(Course.created_at.desc())
        .limit(6)
        .all()
    )
    categories = Category.query.order_by(Category.name).limit(8).all()
    return render_template("main/home.html", featured=featured, categories=categories)


@main_bp.route("/about")
def about():
    return render_template("main/about.html")
