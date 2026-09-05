"""
analytics.py
------------
MODULE 8 - Analytics

Uses pandas/numpy to compute stats: most popular skills, most applied
jobs, average salary, and skill frequency — all consumed by
visualization.py for charts.
"""

import pandas as pd
import numpy as np
from database import get_connection
from job_manager import get_all_jobs


def _extracted_skills_df() -> pd.DataFrame:
    conn = get_connection()
    try:
        return pd.read_sql_query("SELECT * FROM ExtractedSkills", conn)
    finally:
        conn.close()


def _applications_df() -> pd.DataFrame:
    conn = get_connection()
    try:
        return pd.read_sql_query("""
            SELECT Applications.*, Jobs.title, Jobs.company
            FROM Applications JOIN Jobs ON Applications.job_id = Jobs.id
        """, conn)
    finally:
        conn.close()


def most_popular_skills(top_n: int = 10) -> pd.Series:
    """Across ALL users, which extracted skills show up most often?"""
    df = _extracted_skills_df()
    if df.empty:
        return pd.Series(dtype=int)
    return df["skill"].value_counts().head(top_n)


def most_applied_jobs(top_n: int = 10) -> pd.Series:
    """Which jobs have the most saved applications?"""
    df = _applications_df()
    if df.empty:
        return pd.Series(dtype=int)
    return df["title"].value_counts().head(top_n)


def average_salary() -> float:
    """Average salary across all jobs in the database, using numpy for the calc."""
    jobs = get_all_jobs()
    salaries = [j["salary"] for j in jobs if j["salary"]]
    if not salaries:
        return 0.0
    return float(np.mean(salaries))


def skill_frequency_by_category() -> pd.Series:
    """How many distinct skills were detected per category (language/database/framework/ai)."""
    df = _extracted_skills_df()
    if df.empty:
        return pd.Series(dtype=int)
    return df["category"].value_counts()


def salary_stats() -> dict:
    """Min / max / mean / median salary — handy single call for a dashboard summary."""
    jobs = get_all_jobs()
    salaries = np.array([j["salary"] for j in jobs if j["salary"]])
    if salaries.size == 0:
        return {"min": 0, "max": 0, "mean": 0, "median": 0}
    return {
        "min": int(salaries.min()),
        "max": int(salaries.max()),
        "mean": round(float(salaries.mean()), 2),
        "median": float(np.median(salaries)),
    }
