"""
job_manager.py
---------------
MODULE 5 - Job Management

View, search, filter, and save jobs. Jobs can come from manual entry
or from the scraper (Module 10).
"""

import json
from datetime import datetime
from database import get_connection


def add_job(title: str, company: str, location: str, salary: int,
            required_skills: list, source: str = "manual") -> dict:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Jobs (title, company, location, salary, required_skills, source)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (title, company, location, salary, json.dumps(required_skills), source))
        conn.commit()
        return {"success": True, "job_id": cur.lastrowid}
    finally:
        conn.close()


def get_all_jobs() -> list:
    """Return every job as a list of dicts, with required_skills already parsed to a list."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Jobs")
        jobs = []
        for row in cur.fetchall():
            job = dict(row)
            job["required_skills"] = json.loads(job["required_skills"])
            jobs.append(job)
        return jobs
    finally:
        conn.close()


def search_jobs(keyword: str) -> list:
    """Search jobs by title or company (case-insensitive substring match)."""
    keyword = f"%{keyword.lower()}%"
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM Jobs
            WHERE LOWER(title) LIKE ? OR LOWER(company) LIKE ?
        """, (keyword, keyword))
        jobs = []
        for row in cur.fetchall():
            job = dict(row)
            job["required_skills"] = json.loads(job["required_skills"])
            jobs.append(job)
        return jobs
    finally:
        conn.close()


def filter_jobs(location: str = None, min_salary: int = None, max_salary: int = None) -> list:
    """Filter jobs by location and/or salary range. Any argument left as None is ignored."""
    query = "SELECT * FROM Jobs WHERE 1=1"
    params = []

    if location:
        query += " AND LOWER(location) = ?"
        params.append(location.lower())
    if min_salary is not None:
        query += " AND salary >= ?"
        params.append(min_salary)
    if max_salary is not None:
        query += " AND salary <= ?"
        params.append(max_salary)

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(query, params)
        jobs = []
        for row in cur.fetchall():
            job = dict(row)
            job["required_skills"] = json.loads(job["required_skills"])
            jobs.append(job)
        return jobs
    finally:
        conn.close()


def save_application(user_id: int, job_id: int, match_percent: float) -> dict:
    """Record that a user applied/saved a job, along with their match % at the time."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Applications (user_id, job_id, match_percent, applied_at)
            VALUES (?, ?, ?, ?)
        """, (user_id, job_id, match_percent, datetime.now().isoformat()))
        conn.commit()
        return {"success": True, "message": "Application saved."}
    finally:
        conn.close()


def get_applications(user_id: int) -> list:
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT Applications.*, Jobs.title, Jobs.company
            FROM Applications JOIN Jobs ON Applications.job_id = Jobs.id
            WHERE Applications.user_id = ?
        """, (user_id,))
        return [dict(row) for row in cur.fetchall()]
    finally:
        conn.close()
