"""
app/utils/template_helpers.py
──────────────────────────────
Jinja2 filters and context processors registered on the app.
Import and call register_helpers(app) from the factory if needed,
or register directly via the blueprint / app.
"""
from datetime import datetime


def timeago(dt: datetime) -> str:
    """Human-friendly relative time string."""
    if not dt:
        return "—"
    now = datetime.utcnow()
    diff = now - dt.replace(tzinfo=None) if dt.tzinfo else now - dt
    seconds = int(diff.total_seconds())
    if seconds < 60:
        return "just now"
    minutes = seconds // 60
    if minutes < 60:
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    days = hours // 24
    if days < 30:
        return f"{days} day{'s' if days != 1 else ''} ago"
    months = days // 30
    if months < 12:
        return f"{months} month{'s' if months != 1 else ''} ago"
    years = days // 365
    return f"{years} year{'s' if years != 1 else ''} ago"


def register_helpers(app):
    app.jinja_env.filters["timeago"] = timeago

    @app.context_processor
    def inject_globals():
        from app.models.course import Category
        return {
            "nav_categories": Category.query.order_by(Category.name).limit(6).all(),
            "current_year": datetime.utcnow().year,
        }
