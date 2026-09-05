## Smart Career Navigator
 
### Overview
 
Smart Career Navigator is an AI-powered career and skill recommendation
platform built entirely in Python. The project was designed to help
students and early-career professionals bridge the gap between what
skills they currently have and what the job market actually demands.
 
The core idea is simple: a user creates an account, uploads their resume,
and the system automatically reads through it to detect their technical
skills. These detected skills are then compared against a database of
job listings, producing a match percentage for each role along with a
clear list of exactly which skills are missing. This turns an otherwise
vague question — "am I ready for this job?" — into a measurable,
data-backed answer.
 
### Problem It Solves
 
Most students apply for jobs without a clear sense of how well their
skill set actually aligns with what a role requires. Career guidance is
often generic, based on job titles rather than actual technical fit.
Smart Career Navigator addresses this by grounding recommendations in
real extracted data from the user's own resume rather than self-reported
guesses, and by surfacing the specific skill gaps a user would need to
close to become a stronger candidate.
 
### How It Works
 
When a resume is uploaded, the system scans its text using regular
expressions to identify programming languages, databases, frameworks,
and AI/ML tools mentioned within it. These extracted skills are stored
against the user's profile. Separately, the platform maintains a
database of job listings, each tagged with the skills it requires. The
recommendation engine then compares a user's skill set against every
job's requirements, calculates an overlap percentage, and ranks jobs
accordingly — while also listing the specific missing skills for each
one, effectively suggesting a personalized learning path.
 
Beyond recommendations, the platform includes an analytics layer that
aggregates data across all users and jobs — identifying the most common
skills in demand, salary distributions, and application trends — and
visualizes this through charts (bar graphs, pie charts, histograms, line
graphs, and heatmaps).
 
### Key Features
 
- Secure user registration and login with hashed passwords
- User profile management covering education, experience, and career interests
- Resume upload and automatic skill extraction
- A job database supporting search and filtering
- A recommendation engine that computes match percentages and skill gaps
- Data analytics and visual charts summarizing trends across the platform
- A basic web scraping module for collecting job listings
- Background multithreading so the interface stays responsive during heavier operations
- A downloadable text-based report summarizing a user's profile, skills, and job matches
### Technology Used
 
The project is built purely in Python, using SQLite for persistent
storage, Tkinter for the desktop interface, Pandas and NumPy for data
analysis, Matplotlib and Seaborn for visualization, and Requests together
with BeautifulSoup for web scraping. Regular expressions handle skill
detection, and Python's built-in threading module keeps the interface
from freezing during longer operations.
 
### Intended Use
 
This project was built as an academic exercise to demonstrate practical,
end-to-end application of core Python concepts — control flow, functions,
object-oriented programming, exception handling, file handling, SQL,
regular expressions, data analysis, visualization, web scraping, and
multithreading — within a single, cohesive, working application rather
than as isolated exercises.
 
