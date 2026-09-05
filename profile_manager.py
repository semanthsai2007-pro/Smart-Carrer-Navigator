"""
profile_manager.py
-------------------
MODULE 2 - User Profile

Stores education, skills, experience, and career interests for a user.
Uses a Profile class (OOP) and stores structured fields as JSON in SQLite.
"""

import json
from database import get_connection


class Profile:
    """Represents one user's profile in memory."""

    def __init__(self, user_id, full_name="", education=None, skills=None,
                 experience=None, interests=None):
        self.user_id = user_id
        self.full_name = full_name
        self.education = education or {}      # e.g. {"degree": "B.Tech CSE", "year": 2026}
        self.skills = skills or []             # e.g. ["python", "sql"]
        self.experience = experience or []     # e.g. [{"role": "Intern", "months": 3}]
        self.interests = interests or []       # e.g. ["Data Science", "Web Dev"]

    def to_row(self):
        """Serialize for DB storage."""
        return (
            self.user_id,
            self.full_name,
            json.dumps(self.education),
            json.dumps(self.skills),
            json.dumps(self.experience),
            json.dumps(self.interests),
        )

    @staticmethod
    def from_row(row) -> "Profile":
        return Profile(
            user_id=row["user_id"],
            full_name=row["full_name"] or "",
            education=json.loads(row["education"] or "{}"),
            skills=json.loads(row["skills"] or "[]"),
            experience=json.loads(row["experience"] or "[]"),
            interests=json.loads(row["interests"] or "[]"),
        )


def save_profile(profile: Profile) -> dict:
    """Insert or update a user's profile (one profile per user)."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT id FROM Profiles WHERE user_id = ?", (profile.user_id,))
        existing = cur.fetchone()

        if existing:
            cur.execute("""
                UPDATE Profiles SET full_name=?, education=?, skills=?, experience=?, interests=?
                WHERE user_id=?
            """, (profile.full_name, json.dumps(profile.education), json.dumps(profile.skills),
                  json.dumps(profile.experience), json.dumps(profile.interests), profile.user_id))
        else:
            cur.execute("""
                INSERT INTO Profiles (user_id, full_name, education, skills, experience, interests)
                VALUES (?, ?, ?, ?, ?, ?)
            """, profile.to_row())

        conn.commit()
        return {"success": True, "message": "Profile saved."}
    except Exception as e:
        return {"success": False, "message": f"Could not save profile: {e}"}
    finally:
        conn.close()


def get_profile(user_id: int):
    """Fetch a user's profile, or None if they haven't created one yet."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Profiles WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        return Profile.from_row(row) if row else None
    finally:
        conn.close()
