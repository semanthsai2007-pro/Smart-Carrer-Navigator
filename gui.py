"""
gui.py
------
MODULE 12 - GUI

Tkinter desktop interface tying every other module together.
Screens: Login, Register, Dashboard, Profile, Resume Upload, Jobs, Analytics.

Run this file directly to launch the app: python gui.py
"""

import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk

import database
import auth
import profile_manager
import resume_manager
import skill_analyzer
import job_manager
import recommender
import visualization
import reports
import threads

database.init_db()

BG = "#f4f6f9"
PRIMARY = "#2c3e50"
ACCENT = "#2980b9"
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_LABEL = ("Segoe UI", 11)
FONT_BTN = ("Segoe UI", 11, "bold")


class CatalystApp(tk.Tk):
    """Root window. Holds a stack of frames (screens) and swaps between them."""

    def __init__(self):
        super().__init__()
        self.title("Smart Carrer Navigator")
        self.geometry("900x600")
        self.configure(bg=BG)
        self.minsize(800, 550)

        container = tk.Frame(self, bg=BG)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (LoginScreen, RegisterScreen, DashboardScreen, ProfileScreen,
                  ResumeScreen, JobsScreen, AnalyticsScreen):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.place(relwidth=1, relheight=1)

        self.show_frame("LoginScreen")

    def show_frame(self, name):
        frame = self.frames[name]
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.tkraise()


class BaseScreen(tk.Frame):
    """Shared look-and-feel helper for all screens."""

    def __init__(self, parent, app):
        super().__init__(parent, bg=BG)
        self.app = app

    def styled_button(self, parent, text, command):
        return tk.Button(parent, text=text, command=command, font=FONT_BTN,
                          bg=ACCENT, fg="white", activebackground="#3498db",
                          relief="flat", padx=14, pady=6, cursor="hand2")

    def nav_bar(self):
        """Top navigation shown on all logged-in screens."""
        bar = tk.Frame(self, bg=PRIMARY, height=45)
        bar.pack(side="top", fill="x")
        for label, target in [("Dashboard", "DashboardScreen"), ("Profile", "ProfileScreen"),
                               ("Resume", "ResumeScreen"), ("Jobs", "JobsScreen"),
                               ("Analytics", "AnalyticsScreen")]:
            tk.Button(bar, text=label, command=lambda t=target: self.app.show_frame(t),
                      font=FONT_LABEL, bg=PRIMARY, fg="white", relief="flat",
                      activebackground=ACCENT, padx=10).pack(side="left", pady=8)
        tk.Button(bar, text="Logout", command=self.logout,
                  font=FONT_LABEL, bg="#c0392b", fg="white", relief="flat",
                  activebackground="#e74c3c", padx=10).pack(side="right", padx=10, pady=8)

    def logout(self):
        auth.Session.logout()
        self.app.show_frame("LoginScreen")


# ---------------------------------------------------------------- LOGIN
class LoginScreen(BaseScreen):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        wrap = tk.Frame(self, bg=BG)
        wrap.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(wrap, text="🚀 Smart Carrer Navigator", font=FONT_TITLE, bg=BG, fg=PRIMARY).pack(pady=(0, 20))

        tk.Label(wrap, text="Username or Email", font=FONT_LABEL, bg=BG).pack(anchor="w")
        self.identifier = tk.Entry(wrap, width=30, font=FONT_LABEL)
        self.identifier.pack(pady=(0, 10))

        tk.Label(wrap, text="Password", font=FONT_LABEL, bg=BG).pack(anchor="w")
        self.password = tk.Entry(wrap, width=30, show="*", font=FONT_LABEL)
        self.password.pack(pady=(0, 15))
        self.password.bind("<Return>", lambda e: self.do_login())

        self.styled_button(wrap, "Login", self.do_login).pack(fill="x", pady=(0, 8))
        tk.Button(wrap, text="Create an account", command=lambda: app.show_frame("RegisterScreen"),
                  font=FONT_LABEL, bg=BG, fg=ACCENT, relief="flat", cursor="hand2").pack()

    def on_show(self):
        self.identifier.delete(0, tk.END)
        self.password.delete(0, tk.END)
        self.identifier.focus_set()

    def do_login(self):
        result = auth.login_user(self.identifier.get(), self.password.get())
        if result["success"]:
            auth.Session.login(result["user"])
            self.app.show_frame("DashboardScreen")
        else:
            messagebox.showerror("Login failed", result["message"])


# ---------------------------------------------------------------- REGISTER
class RegisterScreen(BaseScreen):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        wrap = tk.Frame(self, bg=BG)
        wrap.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(wrap, text="Create Account", font=FONT_TITLE, bg=BG, fg=PRIMARY).pack(pady=(0, 20))

        self.username = self._field(wrap, "Username")
        self.email = self._field(wrap, "Email")
        self.password = self._field(wrap, "Password", show="*")

        self.styled_button(wrap, "Register", self.do_register).pack(fill="x", pady=(10, 8))
        tk.Button(wrap, text="Back to login", command=lambda: app.show_frame("LoginScreen"),
                  font=FONT_LABEL, bg=BG, fg=ACCENT, relief="flat", cursor="hand2").pack()

    def _field(self, wrap, label, show=None):
        tk.Label(wrap, text=label, font=FONT_LABEL, bg=BG).pack(anchor="w")
        e = tk.Entry(wrap, width=30, font=FONT_LABEL, show=show)
        e.pack(pady=(0, 10))
        return e

    def on_show(self):
        for e in (self.username, self.email, self.password):
            e.delete(0, tk.END)

    def do_register(self):
        result = auth.register_user(self.username.get(), self.email.get(), self.password.get())
        if result["success"]:
            messagebox.showinfo("Success", result["message"] + " Please log in.")
            self.app.show_frame("LoginScreen")
        else:
            messagebox.showerror("Registration failed", result["message"])


# ---------------------------------------------------------------- DASHBOARD
class DashboardScreen(BaseScreen):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.nav_bar()
        self.body = tk.Frame(self, bg=BG)
        self.body.pack(fill="both", expand=True, padx=30, pady=20)

    def on_show(self):
        for w in self.body.winfo_children():
            w.destroy()
        user = auth.Session.current_user
        if not user:
            self.app.show_frame("LoginScreen")
            return

        tk.Label(self.body, text=f"Welcome, {user['username']} 👋", font=FONT_TITLE,
                 bg=BG, fg=PRIMARY).pack(anchor="w", pady=(0, 20))

        skills = skill_analyzer.get_saved_skills(user["id"])
        cards = tk.Frame(self.body, bg=BG)
        cards.pack(fill="x")
        self._stat_card(cards, "Skills Detected", len(skills))
        self._stat_card(cards, "Jobs Available", len(job_manager.get_all_jobs()))
        self._stat_card(cards, "Applications Saved", len(job_manager.get_applications(user["id"])))

        if skills:
            tk.Label(self.body, text="Your top job matches:", font=("Segoe UI", 13, "bold"),
                     bg=BG, fg=PRIMARY).pack(anchor="w", pady=(25, 5))
            matches = recommender.recommend_jobs(skills, top_n=3)
            if matches:
                for m in matches:
                    tk.Label(self.body,
                             text=f"• {m.job['title']} @ {m.job['company']} — {m.match_percent}% match",
                             font=FONT_LABEL, bg=BG).pack(anchor="w")
            else:
                tk.Label(self.body, text="No jobs in the database yet.", font=FONT_LABEL,
                         bg=BG, fg="#7f8c8d").pack(anchor="w")
        else:
            tk.Label(self.body, text="Upload your resume to get job recommendations →",
                     font=FONT_LABEL, bg=BG, fg="#7f8c8d").pack(anchor="w", pady=(25, 0))

    def _stat_card(self, parent, label, value):
        card = tk.Frame(parent, bg="white", padx=20, pady=15, relief="flat", bd=1)
        card.pack(side="left", padx=(0, 15))
        tk.Label(card, text=str(value), font=("Segoe UI", 20, "bold"), bg="white", fg=ACCENT).pack()
        tk.Label(card, text=label, font=("Segoe UI", 10), bg="white", fg="#555").pack()


# ---------------------------------------------------------------- PROFILE
class ProfileScreen(BaseScreen):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.nav_bar()
        self.body = tk.Frame(self, bg=BG)
        self.body.pack(fill="both", expand=True, padx=30, pady=20)

    def on_show(self):
        for w in self.body.winfo_children():
            w.destroy()
        user = auth.Session.current_user
        existing = profile_manager.get_profile(user["id"])

        tk.Label(self.body, text="Edit Profile", font=FONT_TITLE, bg=BG, fg=PRIMARY).pack(anchor="w", pady=(0, 15))

        self.name_e = self._field("Full Name", existing.full_name if existing else "")
        self.degree_e = self._field("Education (degree)", existing.education.get("degree", "") if existing else "")
        self.interests_e = self._field("Career Interests (comma-separated)",
                                        ", ".join(existing.interests) if existing else "")

        self.styled_button(self.body, "Save Profile", self.save).pack(anchor="w", pady=(10, 0))

    def _field(self, label, default=""):
        tk.Label(self.body, text=label, font=FONT_LABEL, bg=BG).pack(anchor="w")
        e = tk.Entry(self.body, width=50, font=FONT_LABEL)
        e.insert(0, default)
        e.pack(anchor="w", pady=(0, 10))
        return e

    def save(self):
        user = auth.Session.current_user
        p = profile_manager.Profile(
            user_id=user["id"],
            full_name=self.name_e.get(),
            education={"degree": self.degree_e.get()},
            interests=[s.strip() for s in self.interests_e.get().split(",") if s.strip()],
        )
        result = profile_manager.save_profile(p)
        messagebox.showinfo("Profile", result["message"])


# ---------------------------------------------------------------- RESUME
class ResumeScreen(BaseScreen):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.nav_bar()
        self.body = tk.Frame(self, bg=BG)
        self.body.pack(fill="both", expand=True, padx=30, pady=20)

    def on_show(self):
        for w in self.body.winfo_children():
            w.destroy()
        tk.Label(self.body, text="Resume Management", font=FONT_TITLE, bg=BG, fg=PRIMARY).pack(anchor="w", pady=(0, 15))

        self.styled_button(self.body, "Upload Resume (.txt)", self.upload).pack(anchor="w", pady=(0, 10))

        self.result_box = tk.Text(self.body, height=15, width=80, font=("Consolas", 10))
        self.result_box.pack(fill="both", expand=True)

        user = auth.Session.current_user
        content = resume_manager.get_resume(user["id"])
        if content:
            self.result_box.insert("1.0", content)

    def upload(self):
        path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if not path:
            return
        user = auth.Session.current_user
        result = resume_manager.upload_resume(user["id"], path)
        if not result["success"]:
            messagebox.showerror("Upload failed", result["message"])
            return

        skill_result = skill_analyzer.save_extracted_skills(user["id"], result["content"])
        self.result_box.delete("1.0", tk.END)
        self.result_box.insert("1.0", result["content"])
        messagebox.showinfo("Success", f"Resume uploaded. {skill_result['message']}")


# ---------------------------------------------------------------- JOBS
class JobsScreen(BaseScreen):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.nav_bar()
        self.body = tk.Frame(self, bg=BG)
        self.body.pack(fill="both", expand=True, padx=30, pady=20)

    def on_show(self):
        for w in self.body.winfo_children():
            w.destroy()
        tk.Label(self.body, text="Job Recommendations", font=FONT_TITLE, bg=BG, fg=PRIMARY).pack(anchor="w", pady=(0, 10))

        search_row = tk.Frame(self.body, bg=BG)
        search_row.pack(fill="x", pady=(0, 10))
        self.search_e = tk.Entry(search_row, width=30, font=FONT_LABEL)
        self.search_e.pack(side="left")
        self.styled_button(search_row, "Search", self.do_search).pack(side="left", padx=8)
        self.styled_button(search_row, "Show Recommendations", self.show_recs).pack(side="left")

        self.listbox = tk.Listbox(self.body, font=FONT_LABEL, height=18)
        self.listbox.pack(fill="both", expand=True)
        self.show_recs()

    def _render(self, lines):
        self.listbox.delete(0, tk.END)
        for line in lines:
            self.listbox.insert(tk.END, line)

    def do_search(self):
        results = job_manager.search_jobs(self.search_e.get())
        self._render([f"{j['title']} @ {j['company']} — {j['location']} — ₹{j['salary']}" for j in results]
                     or ["No jobs found."])

    def show_recs(self):
        user = auth.Session.current_user
        skills = skill_analyzer.get_saved_skills(user["id"])
        if not skills:
            self._render(["Upload a resume first to get personalized recommendations."])
            return
        matches = recommender.recommend_jobs(skills)
        lines = []
        for m in matches:
            missing = ", ".join(m.missing_skills) or "None"
            lines.append(f"{m.match_percent}% | {m.job['title']} @ {m.job['company']} | Missing: {missing}")
        self._render(lines or ["No jobs in the database yet."])


# ---------------------------------------------------------------- ANALYTICS
class AnalyticsScreen(BaseScreen):
    def __init__(self, parent, app):
        super().__init__(parent, app)
        self.nav_bar()
        self.body = tk.Frame(self, bg=BG)
        self.body.pack(fill="both", expand=True, padx=30, pady=20)
        self._chart_ref = None

    def on_show(self):
        for w in self.body.winfo_children():
            w.destroy()
        tk.Label(self.body, text="Analytics & Charts", font=FONT_TITLE, bg=BG, fg=PRIMARY).pack(anchor="w", pady=(0, 10))

        btn_row = tk.Frame(self.body, bg=BG)
        btn_row.pack(fill="x", pady=(0, 10))
        self.styled_button(btn_row, "Refresh Charts", self.refresh_charts).pack(side="left")
        self.styled_button(btn_row, "Generate Reports", self.generate_reports).pack(side="left", padx=8)

        self.status = tk.Label(self.body, text="", font=FONT_LABEL, bg=BG, fg="#7f8c8d")
        self.status.pack(anchor="w")

        self.image_label = tk.Label(self.body, bg=BG)
        self.image_label.pack(pady=10)

    def refresh_charts(self):
        """Runs chart generation on a background thread (Module 11) so the GUI doesn't freeze."""
        self.status.config(text="Generating charts...")
        task = threads.BackgroundTask(visualization.generate_all_charts)
        task.start()
        self._poll_task(task)

    def _poll_task(self, task):
        result = task.poll()
        if result is None:
            self.after(150, lambda: self._poll_task(task))
            return
        status, payload = result
        if status == "error":
            self.status.config(text=f"Error: {payload}")
            return
        self.status.config(text="Charts ready.")
        self._show_image(payload["popular_skills"])

    def _show_image(self, path):
        img = Image.open(path)
        img.thumbnail((600, 350))
        photo = ImageTk.PhotoImage(img)
        self.image_label.configure(image=photo)
        self._chart_ref = photo  # keep a reference so Tkinter doesn't garbage-collect it

    def generate_reports(self):
        user = auth.Session.current_user
        paths = reports.full_report(user["id"], user["username"])
        messagebox.showinfo("Reports generated", "\n".join(paths))


if __name__ == "__main__":
    app = CatalystApp()
    app.mainloop()
