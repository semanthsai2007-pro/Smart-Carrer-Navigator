"""
seed_data.py
------------
Populates the Jobs table with sample listings so the app has data
to recommend against on first run. Safe to re-run — it clears and
re-adds only 'manual' source jobs, leaving scraped jobs untouched.
"""

from database import get_connection, init_db
from job_manager import add_job

SAMPLE_JOBS = [
    ("Python Developer", "TechNova", "Hyderabad", 600000, ["python", "sql", "django"]),
    ("ML Engineer", "AIWorks", "Bangalore", 950000, ["python", "tensorflow", "machine learning", "numpy"]),
    ("Frontend Developer", "WebInc", "Remote", 550000, ["javascript", "react", "css", "html"]),
    ("Data Analyst", "DataCore", "Chennai", 480000, ["python", "sql", "pandas", "numpy"]),
    ("Backend Developer", "ServerSide", "Pune", 700000, ["python", "django", "postgresql"]),
    ("Full Stack Developer", "AppHouse", "Hyderabad", 750000, ["javascript", "react", "node.js", "mongodb"]),
    ("AI Research Intern", "DeepMindLab", "Remote", 300000, ["python", "pytorch", "deep learning", "nlp"]),
    ("Java Developer", "CoreSystems", "Delhi", 650000, ["java", "spring", "mysql"]),
    ("DevOps Engineer", "CloudBase", "Bangalore", 800000, ["python", "sql", "docker"]),
    ("Mobile App Developer", "AppCraft", "Mumbai", 620000, ["kotlin", "java", "firebase"]),
]


def seed():
    init_db()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM Jobs WHERE source = 'manual'")
    conn.commit()
    conn.close()

    for title, company, location, salary, skills in SAMPLE_JOBS:
        add_job(title, company, location, salary, skills, source="manual")

    print(f"Seeded {len(SAMPLE_JOBS)} sample jobs.")


if __name__ == "__main__":
    seed()
