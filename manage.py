"""
manage.py
─────────
Optional Flask CLI wrapper for Heroku / older deployment setups.

More commonly just use:
    flask db init
    flask db migrate -m "initial schema"
    flask db upgrade
    python scripts/seed.py
"""
from dotenv import load_dotenv

load_dotenv()

from flask_migrate import upgrade  # noqa: E402
from app import create_app, db    # noqa: E402
from app.models import *           # noqa: F401,E402  import all models so Migrate sees them

app = create_app()


@app.cli.command("init-db")
def init_db():
    """Drop all tables and recreate from models (dev only)."""
    db.drop_all()
    db.create_all()
    print("Database initialised.")


@app.cli.command("seed-db")
def seed_db():
    """Seed the database with demo data."""
    from scripts.seed import run
    run()
