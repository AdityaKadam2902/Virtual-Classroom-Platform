"""
app/__init__.py
───────────────
Application factory.  Import and call create_app() to build the Flask app.
Extensions are initialised here so they can be imported elsewhere without
creating a circular-import chain.
"""
import logging
from logging.handlers import RotatingFileHandler
import os

from flask import Flask, render_template
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

# ── Extension singletons (uninitialised) ─────────────────────────────────────
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
csrf = CSRFProtect()


def create_app(config_object=None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static",
    )

    # ── Load config ───────────────────────────────────────────────────────────
    if config_object is None:
        from app.config import get_config
        config_object = get_config()
    app.config.from_object(config_object)

    # ── Initialise extensions ─────────────────────────────────────────────────
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "warning"

    # ── Register blueprints ───────────────────────────────────────────────────
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.courses import courses_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(courses_bp, url_prefix="/courses")
    app.register_blueprint(dashboard_bp, url_prefix="/dashboard")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    # ── Error handlers ────────────────────────────────────────────────────────
    _register_error_handlers(app)

    # ── Template helpers ──────────────────────────────────────────────────────
    from app.utils.template_helpers import register_helpers
    register_helpers(app)

    # ── Shell context ─────────────────────────────────────────────────────────
    @app.shell_context_processor
    def make_shell_context():  # noqa: WPS430
        from app.models.user import User
        from app.models.course import Course
        from app.models.enrollment import Enrollment
        from app.models.material import CourseMaterial
        return {"db": db, "User": User, "Course": Course,
                "Enrollment": Enrollment, "CourseMaterial": CourseMaterial}

    # ── Logging (production) ──────────────────────────────────────────────────
    if not app.debug and not app.testing:
        _configure_logging(app)

    return app


# ── Helpers ───────────────────────────────────────────────────────────────────

def _register_error_handlers(app: Flask) -> None:
    @app.errorhandler(400)
    def bad_request(e):
        return render_template("errors/400.html"), 400

    @app.errorhandler(403)
    def forbidden(e):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(413)
    def too_large(e):
        return render_template("errors/413.html"), 413

    @app.errorhandler(500)
    def server_error(e):
        app.logger.error("Server error: %s", e)
        return render_template("errors/500.html"), 500


def _configure_logging(app: Flask) -> None:
    logs_dir = os.path.join(app.instance_path, "logs")
    os.makedirs(logs_dir, exist_ok=True)
    handler = RotatingFileHandler(
        os.path.join(logs_dir, "learnhub.log"),
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
    )
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("LearnHub startup")
