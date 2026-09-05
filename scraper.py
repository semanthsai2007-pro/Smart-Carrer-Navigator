"""
scraper.py
----------
MODULE 10 - Web Scraping

Collects job listings (company, role, salary, location).

NOTE FOR YOUR TEAM: live scraping breaks the moment a job site changes
its HTML, and most real job sites block scrapers anyway. This module
is written to parse a standard job-card HTML structure using requests +
BeautifulSoup — real scraping logic, testable against any local or
live HTML with matching tags (see sample_jobs_page.html for a working
example). Point scrape_jobs_from_url() at a real page with the same
structure and it works unchanged.
"""

import requests
from bs4 import BeautifulSoup
from job_manager import add_job


def scrape_jobs_from_html(html: str) -> list:
    """
    Parse job cards out of HTML. Expects each job as:
    <div class="job-card">
        <h2 class="title">...</h2>
        <span class="company">...</span>
        <span class="location">...</span>
        <span class="salary">...</span>
        <ul class="skills"><li>python</li>...</ul>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    jobs = []

    for card in soup.select(".job-card"):
        title = card.select_one(".title")
        company = card.select_one(".company")
        location = card.select_one(".location")
        salary = card.select_one(".salary")
        skills = [li.get_text(strip=True) for li in card.select(".skills li")]

        salary_digits = "".join(filter(str.isdigit, salary.get_text())) if salary else ""

        job = {
            "title": title.get_text(strip=True) if title else "Unknown",
            "company": company.get_text(strip=True) if company else "Unknown",
            "location": location.get_text(strip=True) if location else "Unknown",
            "salary": int(salary_digits) if salary_digits else 0,
            "required_skills": skills,
        }
        jobs.append(job)

    return jobs


def scrape_jobs_from_url(url: str) -> dict:
    """Fetch a real URL and parse it the same way. Wrapped in try/except for network failures."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return {"success": False, "message": f"Network error: {e}", "jobs": []}

    jobs = scrape_jobs_from_html(response.text)
    return {"success": True, "message": f"Scraped {len(jobs)} jobs.", "jobs": jobs}


def save_scraped_jobs(jobs: list) -> int:
    """Insert scraped jobs into the Jobs table. Returns count inserted."""
    count = 0
    for job in jobs:
        add_job(
            title=job["title"],
            company=job["company"],
            location=job["location"],
            salary=job["salary"],
            required_skills=job["required_skills"],
            source="scraped",
        )
        count += 1
    return count


def run_scrape_and_save(html_or_url: str, is_url: bool = False) -> dict:
    """One-call pipeline: scrape then save to DB. Used by the threading module."""
    if is_url:
        result = scrape_jobs_from_url(html_or_url)
        if not result["success"]:
            return result
        jobs = result["jobs"]
    else:
        jobs = scrape_jobs_from_html(html_or_url)

    saved = save_scraped_jobs(jobs)
    return {"success": True, "message": f"Saved {saved} scraped jobs.", "jobs": jobs}
