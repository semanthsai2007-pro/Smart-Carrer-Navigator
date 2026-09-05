"""
resume_manager.py
------------------
MODULE 3 - Resume Management

Upload / read / save / delete a plain-text resume for a user.
"""

from datetime import datetime
from database import get_connection


def upload_resume(user_id: int, file_path: str) -> dict:
    """Read a .txt resume from disk and store its text content in the database."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except FileNotFoundError:
        return {"success": False, "message": "File not found.", "content": None}
    except PermissionError:
        return {"success": False, "message": "Permission denied reading file.", "content": None}
    except UnicodeDecodeError:
        return {"success": False, "message": "File is not readable as plain text (.txt).", "content": None}

    if not content.strip():
        return {"success": False, "message": "Resume file is empty.", "content": None}

    conn = get_connection()
    try:
        cur = conn.cursor()
        # one resume per user — replace if one already exists
        cur.execute("DELETE FROM Resumes WHERE user_id = ?", (user_id,))
        cur.execute(
            "INSERT INTO Resumes (user_id, file_path, content, uploaded_at) VALUES (?, ?, ?, ?)",
            (user_id, file_path, content, datetime.now().isoformat()),
        )
        conn.commit()
        return {"success": True, "message": "Resume uploaded successfully.", "content": content}
    except Exception as e:
        return {"success": False, "message": f"Database error: {e}", "content": None}
    finally:
        conn.close()


def save_resume_text(user_id: int, content: str) -> dict:
    """Directly save resume text (e.g. pasted into the GUI instead of a file)."""
    if not content.strip():
        return {"success": False, "message": "Resume content is empty."}

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Resumes WHERE user_id = ?", (user_id,))
        cur.execute(
            "INSERT INTO Resumes (user_id, file_path, content, uploaded_at) VALUES (?, ?, ?, ?)",
            (user_id, "(pasted text)", content, datetime.now().isoformat()),
        )
        conn.commit()
        return {"success": True, "message": "Resume saved."}
    finally:
        conn.close()


def get_resume(user_id: int):
    """Return the stored resume text for a user, or None."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT content FROM Resumes WHERE user_id = ?", (user_id,))
        row = cur.fetchone()
        return row["content"] if row else None
    finally:
        conn.close()


def delete_resume(user_id: int) -> dict:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Resumes WHERE user_id = ?", (user_id,))
        conn.commit()
        if cur.rowcount == 0:
            return {"success": False, "message": "No resume found to delete."}
        return {"success": True, "message": "Resume deleted."}
    finally:
        conn.close()
