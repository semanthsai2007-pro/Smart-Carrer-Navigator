"""
visualization.py
-----------------
MODULE 9 - Visualization

Generates charts (pie, bar, line, heatmap, histogram) from analytics.py
data using Matplotlib/Seaborn, and saves them as PNGs the GUI can display.
"""

import os
import matplotlib
matplotlib.use("Agg")  # safe non-interactive backend; GUI embeds the saved PNG
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

import analytics
from job_manager import get_all_jobs

CHART_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "charts")
os.makedirs(CHART_DIR, exist_ok=True)

sns.set_theme(style="whitegrid")


def _save(fig, filename):
    path = os.path.join(CHART_DIR, filename)
    fig.savefig(path, bbox_inches="tight", dpi=120)
    plt.close(fig)
    return path


def chart_popular_skills_bar(top_n=10):
    """Bar chart: most popular skills across all users."""
    series = analytics.most_popular_skills(top_n)
    fig, ax = plt.subplots(figsize=(7, 4))
    if series.empty:
        ax.text(0.5, 0.5, "No skill data yet", ha="center", va="center")
    else:
        sns.barplot(x=series.values, y=series.index, hue=series.index, ax=ax,
                    palette="viridis", legend=False)
        ax.set_xlabel("Users with this skill")
        ax.set_title("Most Popular Skills")
    return _save(fig, "popular_skills_bar.png")


def chart_skill_category_pie():
    """Pie chart: proportion of detected skills per category."""
    series = analytics.skill_frequency_by_category()
    fig, ax = plt.subplots(figsize=(5, 5))
    if series.empty:
        ax.text(0.5, 0.5, "No skill data yet", ha="center", va="center")
    else:
        ax.pie(series.values, labels=series.index, autopct="%1.1f%%", startangle=90)
        ax.set_title("Skill Categories")
    return _save(fig, "skill_category_pie.png")


def chart_salary_histogram():
    """Histogram: distribution of job salaries."""
    jobs = get_all_jobs()
    salaries = [j["salary"] for j in jobs if j["salary"]]
    fig, ax = plt.subplots(figsize=(7, 4))
    if not salaries:
        ax.text(0.5, 0.5, "No job data yet", ha="center", va="center")
    else:
        sns.histplot(salaries, bins=10, kde=True, ax=ax, color="steelblue")
        ax.set_xlabel("Salary")
        ax.set_title("Salary Distribution")
    return _save(fig, "salary_histogram.png")


def chart_applied_jobs_line():
    """Line chart: number of applications over time (by day)."""
    df = analytics._applications_df()
    fig, ax = plt.subplots(figsize=(7, 4))
    if df.empty:
        ax.text(0.5, 0.5, "No applications yet", ha="center", va="center")
    else:
        df["applied_at"] = pd.to_datetime(df["applied_at"])
        daily = df.groupby(df["applied_at"].dt.date).size()
        daily.plot(kind="line", marker="o", ax=ax, color="darkorange")
        ax.set_ylabel("Applications")
        ax.set_title("Applications Over Time")
    return _save(fig, "applications_line.png")


def chart_skill_job_heatmap():
    """Heatmap: which skills are required across which jobs (1 = required)."""
    jobs = get_all_jobs()
    fig, ax = plt.subplots(figsize=(8, 5))
    if not jobs:
        ax.text(0.5, 0.5, "No job data yet", ha="center", va="center")
    else:
        all_skills = sorted({s for j in jobs for s in j["required_skills"]})
        matrix = pd.DataFrame(
            [[1 if s in j["required_skills"] else 0 for s in all_skills] for j in jobs],
            index=[j["title"] for j in jobs],
            columns=all_skills,
        )
        sns.heatmap(matrix, cmap="YlGnBu", cbar=True, ax=ax)
        ax.set_title("Skill Requirements by Job")
    return _save(fig, "skill_job_heatmap.png")


def generate_all_charts() -> dict:
    """Convenience function the GUI/reports can call to refresh every chart at once."""
    return {
        "popular_skills": chart_popular_skills_bar(),
        "skill_category": chart_skill_category_pie(),
        "salary_histogram": chart_salary_histogram(),
        "applications_line": chart_applied_jobs_line(),
        "skill_heatmap": chart_skill_job_heatmap(),
    }
