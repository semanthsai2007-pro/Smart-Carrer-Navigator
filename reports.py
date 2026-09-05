"""
reports.py
----------
MODULE 13 - Reports

Generates plain-text reports: user report, skill report, job report,
analytics report.
"""

import os
from datetime import datetime

import analytics
from profile_manager import get_profile
from skill_analyzer import get_saved_skills
from job_manager import get_all_jobs

REPORT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports_output")
os.makedirs(REPORT_DIR, exist_ok=True)


def _write(filename, lines):
    path = os.path.join(REPORT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path


def user_report(user_id: int, username: str) -> str:
    profile = get_profile(user_id)
    lines = [
        f"USER REPORT - {username}",
        f"Generated: {datetime.now().isoformat()}",
        "-" * 40,
    ]
    if profile:
        lines += [
            f"Full name: {profile.full_name}",
            f"Education: {profile.education}",
            f"Skills (self-reported): {', '.join(profile.skills) or 'None'}",
            f"Experience: {profile.experience}",
            f"Interests: {', '.join(profile.interests) or 'None'}",
        ]
    else:
        lines.append("No profile created yet.")
    return _write(f"user_report_{user_id}.txt", lines)


def skill_report(user_id: int) -> str:
    skills = get_saved_skills(user_id)
    lines = [
        "SKILL REPORT",
        f"Generated: {datetime.now().isoformat()}",
        "-" * 40,
        f"Total skills detected: {len(skills)}",
        f"Skills: {', '.join(sorted(skills)) if skills else 'None detected yet'}",
    ]
    return _write(f"skill_report_{user_id}.txt", lines)


def job_report() -> str:
    jobs = get_all_jobs()
    lines = ["JOB REPORT", f"Generated: {datetime.now().isoformat()}", "-" * 40,
              f"Total jobs listed: {len(jobs)}", ""]
    for j in jobs:
        lines.append(f"- {j['title']} @ {j['company']} ({j['location']}) | Salary: {j['salary']}")
        lines.append(f"  Required: {', '.join(j['required_skills'])}")
    return _write("job_report.txt", lines)


def analytics_report() -> str:
    lines = ["ANALYTICS REPORT", f"Generated: {datetime.now().isoformat()}", "-" * 40]

    popular = analytics.most_popular_skills()
    lines.append("Most popular skills:")
    lines += [f"  {skill}: {count}" for skill, count in popular.items()] or ["  No data"]

    stats = analytics.salary_stats()
    lines.append("")
    lines.append(f"Salary stats: min={stats['min']} max={stats['max']} "
                  f"mean={stats['mean']} median={stats['median']}")

    return _write("analytics_report.txt", lines)


def full_report(user_id: int, username: str) -> list:
    """Generate all four reports at once. Returns list of file paths."""
    return [
        user_report(user_id, username),
        skill_report(user_id),
        job_report(),
        analytics_report(),
    ]
