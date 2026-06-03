"""
run.py
──────
Application entry point.

Development:
    python run.py

Production (gunicorn):
    gunicorn "run:app" --workers 4 --bind 0.0.0.0:8000
"""
from dotenv import load_dotenv

load_dotenv()  # load .env before anything else reads os.environ

from app import create_app  # noqa: E402

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
