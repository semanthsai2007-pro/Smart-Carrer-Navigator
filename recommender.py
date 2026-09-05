"""
recommender.py
---------------
MODULE 6 - Recommendation Engine

Matches a user's skills against every job's required skills,
computes a match percentage, lists missing skills, and suggests
a simple learning path for the gap.
"""

from job_manager import get_all_jobs


class JobMatch:
    """OOP wrapper for one job's match result — makes GUI/report code read cleanly."""

    def __init__(self, job: dict, match_percent: float, matched_skills: set, missing_skills: set):
        self.job = job
        self.match_percent = match_percent
        self.matched_skills = matched_skills
        self.missing_skills = missing_skills

    def learning_path(self) -> list:
        """Very simple suggestion: just the missing skills, ordered alphabetically."""
        return sorted(self.missing_skills)

    def __repr__(self):
        return f"<JobMatch {self.job['title']} @ {self.job['company']} - {self.match_percent}%>"


def calculate_match(user_skills: set, job_required_skills: list):
    """Pure function: given a user's skill set and one job's required skills, compute the match."""
    required = {s.lower() for s in job_required_skills}
    user_skills_lower = {s.lower() for s in user_skills}

    if not required:
        return None

    matched = user_skills_lower & required
    missing = required - user_skills_lower
    percent = round((len(matched) / len(required)) * 100, 1)

    return matched, missing, percent


def recommend_jobs(user_skills: set, top_n: int = 10) -> list:
    """
    Return the top N job matches for a user, sorted by match percentage (highest first).
    """
    jobs = get_all_jobs()
    results = []

    for job in jobs:
        match_result = calculate_match(user_skills, job["required_skills"])
        if match_result is None:
            continue
        matched, missing, percent = match_result
        results.append(JobMatch(job, percent, matched, missing))

    results.sort(key=lambda jm: jm.match_percent, reverse=True)
    return results[:top_n]
