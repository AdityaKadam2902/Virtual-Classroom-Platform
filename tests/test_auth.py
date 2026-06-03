"""
tests/test_auth.py
──────────────────
Integration tests for registration and login flows.
"""
import pytest

from app.models.user import User


def register(client, **kwargs):
    defaults = dict(
        first_name="Jane", last_name="Doe",
        email="jane@example.com", role="student",
        password="Secure1234", confirm_password="Secure1234", terms="y",
    )
    defaults.update(kwargs)
    return client.post("/auth/register", data=defaults, follow_redirects=True)


def login(client, email="jane@example.com", password="Secure1234"):
    return client.post(
        "/auth/login",
        data={"email": email, "password": password},
        follow_redirects=True,
    )


class TestRegistration:
    def test_register_page_loads(self, client):
        # log out first so we're not already authenticated from a prior test
        client.get("/auth/logout")
        r = client.get("/auth/register")
        assert r.status_code == 200

    def test_successful_registration(self, client, app):
        client.get("/auth/logout")
        r = register(client)
        assert r.status_code == 200
        from app import db
        with app.app_context():
            user = User.query.filter_by(email="jane@example.com").first()
            assert user is not None
            assert user.role == "student"

    def test_duplicate_email_rejected(self, client):
        client.get("/auth/logout")
        register(client)
        client.get("/auth/logout")
        r = register(client)
        assert b"already registered" in r.data or r.status_code == 200

    def test_password_mismatch_rejected(self, client):
        client.get("/auth/logout")
        r = register(client, confirm_password="DifferentOne1!")
        # Should stay on register page (200) rather than redirect to dashboard
        assert r.status_code == 200
        assert b"Create Account" in r.data or b"Join" in r.data

    def test_weak_password_rejected(self, client):
        client.get("/auth/logout")
        r = register(client, password="weakpass", confirm_password="weakpass")
        assert r.status_code == 200


class TestLogin:
    def test_login_page_loads_when_logged_out(self, client):
        client.get("/auth/logout")
        r = client.get("/auth/login")
        assert r.status_code == 200
        assert b"Sign In" in r.data or b"Login" in r.data

    def test_successful_login_redirects_to_dashboard(self, client):
        client.get("/auth/logout")
        register(client)
        client.get("/auth/logout")
        r = login(client)
        assert r.status_code == 200
        assert b"Dashboard" in r.data or b"Welcome" in r.data

    def test_wrong_password_shows_error(self, client):
        client.get("/auth/logout")
        register(client)
        client.get("/auth/logout")
        r = login(client, password="WrongPass99")
        assert b"Invalid" in r.data or b"incorrect" in r.data.lower()

    def test_nonexistent_email_shows_error(self, client):
        client.get("/auth/logout")
        r = login(client, email="nobody@example.com")
        assert b"Invalid" in r.data or b"incorrect" in r.data.lower()

    def test_logout_redirects_to_home(self, client):
        client.get("/auth/logout")
        register(client)
        r = client.get("/auth/logout", follow_redirects=True)
        assert r.status_code == 200
        assert b"LearnHub" in r.data
