"""
skill_analyzer.py
------------------
MODULE 4 - Skill Analyzer

Scans resume text with regex and detects skills, split into categories:
languages, databases, frameworks, and AI/ML tools.
"""

import re
from database import get_connection

# Keyword banks — easy for teammates to extend later.
SKILL_BANK = {
    "language": [
        "python", "java", "c\\+\\+", "c#", "javascript", "typescript", "sql",
        "html", "css", "r", "go", "kotlin", "swift", "php", "ruby",
    ],
    "database": [
        "mysql", "postgresql", "sqlite", "mongodb", "oracle", "firebase",
        "redis", "cassandra", "mariadb",
    ],
    "framework": [
        "django", "flask", "react", "angular", "vue", "spring", "node\\.?js",
        "tkinter", "fastapi", "express", "bootstrap", "\\.net",
    ],
    "ai": [
        "machine learning", "deep learning", "tensorflow", "pytorch",
        "scikit-learn", "keras", "nlp", "opencv", "pandas", "numpy",
        "artificial intelligence", "neural network",
    ],
}


def extract_skills(resume_text: str) -> dict:
    """
    Scan resume_text and return detected skills grouped by category:
    {"language": [...], "database": [...], "framework": [...], "ai": [...]}
    Uses word-boundary regex so 'r' doesn't match inside 'framework', etc.
    """
    text = resume_text.lower()
    found = {category: set() for category in SKILL_BANK}

    for category, keywords in SKILL_BANK.items():
        for kw in keywords:
            pattern = r"\b" + kw + r"\b"
            if re.search(pattern, text):
                clean = kw.replace("\\", "")  # undo regex escaping like \+\+ -> ++
                found[category].add(clean)

    return {cat: sorted(skills) for cat, skills in found.items()}


def get_all_skills_flat(resume_text: str) -> set:
    """Return every detected skill as one flat set, regardless of category."""
    grouped = extract_skills(resume_text)
    flat = set()
    for skills in grouped.values():
        flat.update(skills)
    return flat


def save_extracted_skills(user_id: int, resume_text: str) -> dict:
    """Extract skills from resume text and persist them to ExtractedSkills table."""
    grouped = extract_skills(resume_text)

    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM ExtractedSkills WHERE user_id = ?", (user_id,))
        for category, skills in grouped.items():
            for skill in skills:
                cur.execute(
                    "INSERT INTO ExtractedSkills (user_id, skill, category) VALUES (?, ?, ?)",
                    (user_id, skill, category),
                )
        conn.commit()
        total = sum(len(s) for s in grouped.values())
        return {"success": True, "message": f"{total} skills detected.", "skills": grouped}
    finally:
        conn.close()


def get_saved_skills(user_id: int) -> set:
    """Fetch previously-extracted skills for a user as a flat set."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT skill FROM ExtractedSkills WHERE user_id = ?", (user_id,))
        return {row["skill"] for row in cur.fetchall()}
    finally:
        conn.close()
