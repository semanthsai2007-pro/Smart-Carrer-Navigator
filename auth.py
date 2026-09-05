"""
auth.py
-------
MODULE 1 - User Authentication

Handles registration, login, logout.
Passwords are never stored in plain text (SHA-256 hash).
"""

import hashlib
import re
from datetime import datetime
from database import get_connection


def _hash_password(password: str) -> str:
    """Hash a password with SHA-256. Simple + dependency-free, good enough for a student project."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def _valid_email(email: str) -> bool:
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))


def register_user(username: str, email: str, password: str) -> dict:
    """
    Create a new user account.
    Returns {"success": bool, "message": str, "user_id": int|None}
    """
    username = username.strip()
    email = email.strip().lower()

    if not username or not email or not password:
        return {"success": False, "message": "All fields are required.", "user_id": None}
    if not _valid_email(email):
        return {"success": False, "message": "Invalid email format.", "user_id": None}
    if len(password) < 6:
        return {"success": False, "message": "Password must be at least 6 characters.", "user_id": None}

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Users (username, email, password_hash, created_at) VALUES (?, ?, ?, ?)",
            (username, email, _hash_password(password), datetime.now().isoformat()),
        )
        conn.commit()
        user_id = cur.lastrowid
        return {"success": True, "message": "Registration successful.", "user_id": user_id}
    except Exception as e:
        # Catches UNIQUE constraint violations (duplicate username/email) and any other DB error
        if "UNIQUE" in str(e):
            return {"success": False, "message": "Username or email already exists.", "user_id": None}
        return {"success": False, "message": f"Registration failed: {e}", "user_id": None}
    finally:
        conn.close()


def login_user(identifier: str, password: str) -> dict:
    """
    Log in with username OR email + password.
    Returns {"success": bool, "message": str, "user": dict|None}
    """
    identifier = identifier.strip()
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM Users WHERE username = ? OR email = ?",
            (identifier, identifier.lower()),
        )
        user = cur.fetchone()

        if user is None:
            return {"success": False, "message": "No account found with that username/email.", "user": None}

        if user["password_hash"] != _hash_password(password):
            return {"success": False, "message": "Incorrect password.", "user": None}

        return {"success": True, "message": f"Welcome back, {user['username']}!", "user": dict(user)}
    except Exception as e:
        return {"success": False, "message": f"Login failed: {e}", "user": None}
    finally:
        conn.close()


def reset_password(email: str, new_password: str) -> dict:
    """Simple password reset (no email verification — good enough for local/student use)."""
    if len(new_password) < 6:
        return {"success": False, "message": "Password must be at least 6 characters."}

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "UPDATE Users SET password_hash = ? WHERE email = ?",
            (_hash_password(new_password), email.strip().lower()),
        )
        conn.commit()
        if cur.rowcount == 0:
            return {"success": False, "message": "No account with that email."}
        return {"success": True, "message": "Password updated successfully."}
    finally:
        conn.close()


class Session:
    """Tiny in-memory session holder — set on login, cleared on logout."""
    current_user = None

    @classmethod
    def login(cls, user: dict):
        cls.current_user = user

    @classmethod
    def logout(cls):
        cls.current_user = None

    @classmethod
    def is_logged_in(cls) -> bool:
        return cls.current_user is not None
