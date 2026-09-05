"""
main.py
-------
Single entry point for Project Catalyst.

Run this file to:
  1. Initialize the database (creates catalyst.db if it doesn't exist)
  2. Seed sample job listings (only if the Jobs table is empty)
  3. Launch the Tkinter GUI

Usage:
    python main.py
"""

from database import init_db, get_connection
from seed_data import seed
from gui import CatalystApp


def bootstrap():
    init_db()
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as c FROM Jobs")
    count = cur.fetchone()["c"]
    conn.close()

    if count == 0:
        print("No jobs found — seeding sample job listings...")
        seed()


if __name__ == "__main__":
    bootstrap()
    app = CatalystApp()
    app.mainloop()
