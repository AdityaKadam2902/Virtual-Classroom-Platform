"""
app/config.py
─────────────
All configuration comes from environment variables (via .env).
Never hardcode secrets here.
"""
import os
from datetime import timedelta


class BaseConfig:
    # ── Core ──────────────────────────────────────────────────────────────────
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-only-please-change")
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    # ── Database ───────────────────────────────────────────────────────────────
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        "DATABASE_URL", "sqlite:///learnhub.db"
    )

    # ── Session ────────────────────────────────────────────────────────────────
    PERMANENT_SESSION_LIFETIME: timedelta = timedelta(
        minutes=int(os.environ.get("SESSION_LIFETIME_MINUTES", "60"))
    )

    # ── File uploads ──────────────────────────────────────────────────────────
    MAX_CONTENT_LENGTH: int = (
        int(os.environ.get("MAX_CONTENT_LENGTH_MB", "10")) * 1024 * 1024
    )
    ALLOWED_EXTENSIONS: set = {"pdf", "png", "jpg", "jpeg", "gif", "mp4", "zip", "docx", "pptx"}
    STORAGE_BACKEND: str = os.environ.get("STORAGE_BACKEND", "local")  # 'local' | 's3'
    LOCAL_UPLOAD_FOLDER: str = os.environ.get("LOCAL_UPLOAD_FOLDER", "uploads")

    # ── AWS S3 ────────────────────────────────────────────────────────────────
    AWS_ACCESS_KEY_ID: str = os.environ.get("AWS_ACCESS_KEY_ID", "")
    AWS_SECRET_ACCESS_KEY: str = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    AWS_S3_BUCKET: str = os.environ.get("AWS_S3_BUCKET", "")
    AWS_S3_REGION: str = os.environ.get("AWS_S3_REGION", "us-east-1")

    # ── WTF / CSRF ────────────────────────────────────────────────────────────
    WTF_CSRF_ENABLED: bool = True

    # ── Rate limiting ─────────────────────────────────────────────────────────
    RATELIMIT_DEFAULT: str = "200 per day;50 per hour"
    RATELIMIT_STORAGE_URL: str = "memory://"


class DevelopmentConfig(BaseConfig):
    DEBUG: bool = True
    WTF_CSRF_ENABLED: bool = True


class ProductionConfig(BaseConfig):
    DEBUG: bool = False
    TESTING: bool = False

    @classmethod
    def validate(cls) -> None:
        """Fail fast if required production env vars are missing."""
        required = ["SECRET_KEY", "DATABASE_URL"]
        missing = [k for k in required if not os.environ.get(k)]
        if missing:
            raise RuntimeError(
                f"Missing required environment variables: {', '.join(missing)}"
            )


class TestingConfig(BaseConfig):
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"
    WTF_CSRF_ENABLED: bool = False
    SERVER_NAME: str = "localhost"


config_map = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config() -> type:
    env = os.environ.get("FLASK_ENV", "development")
    return config_map.get(env, DevelopmentConfig)
