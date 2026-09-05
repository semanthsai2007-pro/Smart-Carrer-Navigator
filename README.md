# 🚀 Project Catalyst
### AI-Powered Career & Skill Recommendation Platform

A complete Python desktop application: register, upload a resume, get your
skills auto-detected, receive job recommendations with match %, and view
analytics + charts — all through a clean Tkinter GUI.

---

## How to Run

```bash
pip install -r requirements.txt
python main.py
```

First run automatically creates the database (`catalyst.db`) and seeds 10
sample jobs so the app isn't empty. Register an account, then go to
**Resume** and upload `sample_resume.txt` (included) to see it all work end
to end.

---

## Project Structure (mapped to your syllabus modules)

| File | Module | What it does |
|---|---|---|
| `auth.py` | 1 — Authentication | Register, login, logout, password reset (SHA-256 hashed passwords) |
| `profile_manager.py` | 2 — User Profile | Education, skills, experience, interests (OOP `Profile` class) |
| `resume_manager.py` | 3 — Resume Management | Upload/read/save/delete `.txt` resumes |
| `skill_analyzer.py` | 4 — Skill Analyzer | Regex-based skill detection (languages, DBs, frameworks, AI tools) |
| `job_manager.py` | 5 — Job Management | View/search/filter jobs, save applications |
| `recommender.py` | 6 — Recommendation Engine | Match %, missing skills, learning path |
| `database.py` | 7 — Database | All SQLite tables + shared connection |
| `analytics.py` | 8 — Analytics | Pandas/NumPy stats (popular skills, salary stats, etc.) |
| `visualization.py` | 9 — Visualization | Matplotlib/Seaborn: bar, pie, histogram, line, heatmap |
| `scraper.py` | 10 — Web Scraping | requests + BeautifulSoup job-listing parser |
| `threads.py` | 11 — Multithreading | Background thread runner so the GUI never freezes |
| `gui.py` | 12 — GUI | Full Tkinter app: Login, Register, Dashboard, Profile, Resume, Jobs, Analytics |
| `reports.py` | 13 — Reports | Plain-text user/skill/job/analytics reports |
| `seed_data.py` | — | Populates sample jobs on first run |
| `main.py` | — | Single entry point — run this file |

Module 14 (Testing) is up to your team — see "Suggested Test Cases" below.

---

## How the 3 of you can split ownership (matches your earlier plan)

- **Person A — Backend:** `database.py`, `auth.py`, `profile_manager.py`, `resume_manager.py`, `job_manager.py`
- **Person B — Intelligence:** `skill_analyzer.py`, `recommender.py`, `analytics.py`, `scraper.py`
- **Person C — Interface:** `gui.py`, `visualization.py`, `threads.py`, `reports.py`

Everything is already wired together and tested — you can now each read your
files, tweak them, and understand the whole flow without breaking anyone
else's part, since every module only talks to the others through simple
function calls.

---

## Suggested Test Cases (Module 14)

- Register with an already-used username/email → should fail cleanly
- Login with wrong password → should fail cleanly
- Upload an empty `.txt` file → should be rejected
- Upload a non-existent file path → should be rejected
- Recommend jobs with zero extracted skills → should return 0% matches, not crash
- Run `scraper.py` against `sample_jobs_page.html` → should insert exactly 2 jobs
- Generate charts with an empty database → should still render (with a "no data" placeholder), not crash

---

## Extending it further

- Swap `.txt`-only resumes for PDF using `pdfplumber` in `resume_manager.py`
- Point `scraper.scrape_jobs_from_url()` at a real job board with matching HTML structure
- Add more keywords to `SKILL_BANK` in `skill_analyzer.py` as you think of them
- Turn `reports.py` output into a PDF using `fpdf2` instead of plain `.txt`
