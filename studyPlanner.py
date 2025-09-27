import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os
import hashlib

# Global variables
current_user = None
tasks = []

def priority_value(p):
    return {"High": 3, "Medium": 2, "Low": 1}.get(p, 0)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def add_task(subject, topic, deadline, est_time, priority):
    try:
        datetime.strptime(deadline, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Deadline must be in YYYY-MM-DD format")
        return False
    task = {
        "subject": subject,
        "topic": topic,
        "deadline": deadline,
        "est_time": est_time,
        "priority": priority
    }
    tasks.append(task)
    save_user_data()
    return True

def generate_schedule():
    if not tasks:
        return "No tasks to schedule."
    sorted_tasks = sorted(tasks, key=lambda x: (x['deadline'], -priority_value(x['priority'])))
    result = "🎯 Suggested Study Plan:\n"
    grouped = {}
    for task in sorted_tasks:
        date = task['deadline']
        if date not in grouped:
            grouped[date] = []
        grouped[date].append(task)
    for date in sorted(grouped.keys()):
        result += f"\n📅 {date}:\n"
        for t in grouped[date]:
            result += f"  • {t['subject']} - {t['topic']} ({t['est_time']} hrs) | Priority: {t['priority']}\n"
    return result

def show_stats():
    if not tasks:
        return "No tasks to analyze."
    total = len(tasks)
    high = sum(1 for t in tasks if t['priority'] == 'High')
    med = sum(1 for t in tasks if t['priority'] == 'Medium')
    low = sum(1 for t in tasks if t['priority'] == 'Low')
    return f"""📊 Productivity Stats:
Total Tasks: {total}
🔥 High Priority: {high}
🌟 Medium Priority: {med}
🌀 Low Priority: {low}
"""

def save_user_data():
    if current_user:
        with open(f"{current_user}_data.json", "w") as f:
            json.dump(tasks, f)

def load_user_data(username):
    global tasks
    filename = f"{username}_data.json"
    if os.path.exists(filename):
        with open(filename, "r") as f:
            tasks = json.load(f)
    else:
        tasks = []

def save_credentials(username, password):
    if not os.path.exists("users.json"):
        with open("users.json", "w") as f:
            json.dump({}, f)
    with open("users.json", "r") as f:
        users = json.load(f)
    users[username] = hash_password(password)
    with open("users.json", "w") as f:
        json.dump(users, f)

def validate_login(username, password):
    if not os.path.exists("users.json"):
        return False
    with open("users.json", "r") as f:
        users = json.load(f)
    return users.get(username) == hash_password(password)

class LoginPage(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("🔐 Study Planner Login")
        self.geometry("400x300")
        self.configure(bg="#f0f6ff")

        ttk.Label(self, text="📚 AI Study Planner", font=("Segoe UI", 16, "bold")).pack(pady=10)
        ttk.Label(self, text="Username:", font=("Segoe UI", 11)).pack(pady=4)
        self.username_entry = ttk.Entry(self, width=30)
        self.username_entry.pack()
        ttk.Label(self, text="Password:", font=("Segoe UI", 11)).pack(pady=4)
        self.password_entry = ttk.Entry(self, show="*", width=30)
        self.password_entry.pack()
        ttk.Button(self, text="Login", command=self.login).pack(pady=10)
        ttk.Button(self, text="Register", command=self.register).pack()

    def login(self):
        global current_user
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if validate_login(username, password):
            current_user = username
            load_user_data(current_user)
            self.destroy()
            app = StudyPlannerApp()
            app.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

    def register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        if not username or not password:
            messagebox.showwarning("Warning", "Both fields are required.")
            return
        save_credentials(username, password)
        messagebox.showinfo("Registered", "Account created. Please log in.")

class StudyPlannerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("📘 AI Study Planner - Dashboard")
        self.geometry("800x600")
        self.configure(bg="#f9fcff")

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("TNotebook.Tab", font=("Segoe UI", 10), padding=[10, 5])
        self.style.configure("TButton", font=("Segoe UI", 10))
        self.style.configure("TLabel", font=("Segoe UI", 10))

        self.create_widgets()

    def create_widgets(self):
        header = tk.Label(self, text=f"Welcome, {current_user} 👋", font=("Segoe UI", 14, "bold"), bg="#dff0ff", fg="#333")
        header.pack(fill="x", pady=(0, 5))

        self.status_label = tk.Label(self, text=f"📝 Total Tasks: {len(tasks)}    | 👩‍💻 Made by Bisma Nadeem", bg="#e6f2ff", font=("Segoe UI", 9), anchor='w')
        self.status_label.pack(side="bottom", fill="x")

        tab_control = ttk.Notebook(self)
        self.tab_home = ttk.Frame(tab_control)
        self.tab_add = ttk.Frame(tab_control)
        self.tab_view = ttk.Frame(tab_control)
        self.tab_schedule = ttk.Frame(tab_control)
        self.tab_stats = ttk.Frame(tab_control)

        tab_control.add(self.tab_home, text="🏠 Home")
        tab_control.add(self.tab_add, text="➕ Add Task")
        tab_control.add(self.tab_view, text="📋 View")
        tab_control.add(self.tab_schedule, text="📆 Plan")
        tab_control.add(self.tab_stats, text="📊 Stats")
        tab_control.pack(expand=1, fill="both")

        self.create_home_tab()
        self.create_add_tab()
        self.create_view_tab()
        self.create_schedule_tab()
        self.create_stats_tab()

    def create_home_tab(self):
        ttk.Label(self.tab_home, text='"Plan smart, study hard, and success will follow!"', font=("Segoe UI", 12), wraplength=500, justify="center").pack(pady=30)
        ttk.Label(self.tab_home, text="– Your AI Assistant 🤖", font=("Segoe UI", 10)).pack()

    def create_add_tab(self):
        frame = self.tab_add
        self.subject_entry = ttk.Entry(frame, width=30)
        self.topic_entry = ttk.Entry(frame, width=30)
        self.deadline_entry = ttk.Entry(frame, width=30)
        self.est_time_entry = ttk.Entry(frame, width=30)
        self.priority_combo = ttk.Combobox(frame, values=["High", "Medium", "Low"], state="readonly")
        self.priority_combo.current(1)

        fields = ["Subject", "Topic", "Deadline (YYYY-MM-DD)", "Estimated Time (hrs)", "Priority"]
        entries = [self.subject_entry, self.topic_entry, self.deadline_entry, self.est_time_entry, self.priority_combo]
        for i, field in enumerate(fields):
            ttk.Label(frame, text=field).grid(row=i, column=0, padx=10, pady=5, sticky='w')
            entries[i].grid(row=i, column=1, padx=10, pady=5)

        ttk.Button(frame, text="Add Task", command=self.handle_add_task).grid(row=5, column=0, columnspan=2, pady=15)

    def handle_add_task(self):
        subject = self.subject_entry.get().strip()
        topic = self.topic_entry.get().strip()
        deadline = self.deadline_entry.get().strip()
        est_time = self.est_time_entry.get().strip()
        priority = self.priority_combo.get()

        if not all([subject, topic, deadline, est_time, priority]):
            messagebox.showwarning("Warning", "All fields are required.")
            return
        try:
            est_time = int(est_time)
        except ValueError:
            messagebox.showerror("Error", "Estimated time must be a number.")
            return

        if add_task(subject, topic, deadline, est_time, priority):
            messagebox.showinfo("Success", "Task added.")
            self.clear_add_form()
            self.update_all_tabs()

    def clear_add_form(self):
        self.subject_entry.delete(0, tk.END)
        self.topic_entry.delete(0, tk.END)
        self.deadline_entry.delete(0, tk.END)
        self.est_time_entry.delete(0, tk.END)
        self.priority_combo.current(1)

    def create_view_tab(self):
        self.view_frame = tk.Frame(self.tab_view)
        self.view_frame.pack(fill="both", expand=True)
        self.update_view_tab()

    def update_view_tab(self):
        for widget in self.view_frame.winfo_children():
            widget.destroy()
        if not tasks:
            ttk.Label(self.view_frame, text="No tasks available.").pack(pady=20)
            return
        for i, task in enumerate(tasks):
            var = tk.IntVar()
            cb = tk.Checkbutton(
                self.view_frame,
                text=f"{task['subject']} - {task['topic']} | Deadline: {task['deadline']} | {task['est_time']} hrs | {task['priority']}",
                variable=var,
                anchor="w", justify="left", wraplength=700,
                command=lambda i=i, v=var: self.confirm_task_done(i, v)
            )
            cb.pack(anchor="w", padx=10, pady=5)

    def confirm_task_done(self, index, var):
        if var.get() == 1:
            task = tasks[index]
            if messagebox.askyesno("Done?", f"Mark this as complete?\n\n{task['subject']} - {task['topic']}"):
                del tasks[index]
                save_user_data()
                self.update_all_tabs()
            else:
                var.set(0)

    def create_schedule_tab(self):
        self.schedule_text = tk.Text(self.tab_schedule, wrap='word')
        self.schedule_text.pack(expand=True, fill='both')
        self.update_schedule_tab()

    def update_schedule_tab(self):
        self.schedule_text.delete("1.0", tk.END)
        self.schedule_text.insert(tk.END, generate_schedule())

    def create_stats_tab(self):
        self.stats_text = tk.Text(self.tab_stats, wrap='word')
        self.stats_text.pack(expand=True, fill='both')
        self.update_stats_tab()

    def update_stats_tab(self):
        self.stats_text.delete("1.0", tk.END)
        self.stats_text.insert(tk.END, show_stats())

    def update_all_tabs(self):
        self.update_view_tab()
        self.update_schedule_tab()
        self.update_stats_tab()
        self.status_label.config(text=f"📝 Total Tasks: {len(tasks)}    | 👩‍💻 Made by Bisma Nadeem")

if __name__ == "__main__":
    LoginPage().mainloop()

