import os
import sqlite3

DB_FILE = "habit_tracker.db"

# ✅ Ensure Database is Created Before UI Loads
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS habit_list (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    category TEXT CHECK(category IN ('Daily', 'Weekly', 'Quarterly', 'Other'))
                )''')
    c.execute('''CREATE TABLE IF NOT EXISTS habit_progress (
                    date TEXT,
                    habit_id INTEGER,
                    completed INTEGER DEFAULT 0,
                    FOREIGN KEY (habit_id) REFERENCES habit_list(id),
                    PRIMARY KEY (date, habit_id)
                )''')
    conn.commit()
    conn.close()

# ✅ Call this function at the very start!
init_db()

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.ticker as ticker

# Database File
DB_FILE = "habit_tracker.db"

# ✅ Function 1: Initialize Database (Create Tables)
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Ensure habit_list table exists
    c.execute('''CREATE TABLE IF NOT EXISTS habit_list (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE,
                    category TEXT CHECK(category IN ('Daily', 'Weekly', 'Quarterly', 'Other'))
                )''')

    # Ensure habit_progress table exists
    c.execute('''CREATE TABLE IF NOT EXISTS habit_progress (
                    date TEXT,
                    habit_id INTEGER,
                    completed INTEGER DEFAULT 0,
                    FOREIGN KEY (habit_id) REFERENCES habit_list(id),
                    PRIMARY KEY (date, habit_id)
                )''')

    conn.commit()
    conn.close()

# ✅ Function 2: Load Default Habits (Only if Empty)
def load_default_habits():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM habit_list")
    count = c.fetchone()[0]

    if count == 0:  # Only insert if empty
        default_habits = [
            ("Meditation - 15 Min Dawn & 15 Min Dusk", "Daily"),
            ("WELL BEING - Meditate, Exercise", "Daily"),
            ("WORK out - Have you done 30 Min", "Daily"),
            ("Walk - Have you walked 7 KM", "Daily"),
            ("READ - Goal Card, Affirmations", "Daily"),
            ("READ - At least 30 Min on Domain", "Daily"),
            ("PRESENT - Can you Present your learning in today's call?", "Daily"),
            ("Connect - Family, Networking", "Daily"),
            ("Family - Have you called up 1 Friend & 1 Family person?", "Daily"),
            ("Network - Have you posted an Article in Social Media?", "Daily"),
            ("EXCEL - Are you on track: 1 Book, 4 Hr Meditation, 8 Hr Walk & Workout", "Weekly"),
            ("REFINE - Have you got a new idea & shared it with your colleague?", "Weekly"),
            ("REVIEW - Submit ideas, improve communication, explore Biz opportunities", "Weekly"),
            ("REFLECT - Journal Reflection", "Weekly"),
            ("Goal - Short & Long Term Goal finalization & poster", "Quarterly"),
            ("Plan - To reach the target with WBS", "Quarterly"),
            ("Contribute - Return back to society", "Quarterly"),
        ]
        c.executemany("INSERT INTO habit_list (name, category) VALUES (?, ?)", default_habits)
        conn.commit()
    conn.close()

# ✅ Function 3: Fetch Habits from Database
def load_habits():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT id, name, category FROM habit_list ORDER BY category")
    habits = c.fetchall()
    conn.close()
    return habits

# ✅ Function 4: Save Progress
def save_progress():
    selected_date = f"{year_var.get()}-{month_var.get()}-{day_var.get()}"
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    for habit_id, var in habit_vars.items():
        completed = var.get()
        c.execute("INSERT OR REPLACE INTO habit_progress VALUES (?, ?, ?)", (selected_date, habit_id, completed))

    conn.commit()
    conn.close()
    messagebox.showinfo("Success", f"Progress saved for {selected_date}!")

# ✅ Function 5: View Progress (Graph)
def view_progress():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT date, SUM(completed) FROM habit_progress GROUP BY date ORDER BY date")
    data = c.fetchall()
    conn.close()

    if not data:
        messagebox.showwarning("No Data", "No progress data available!")
        return

    dates, completed_counts = zip(*data)

    plt.figure(figsize=(7, 4))
    plt.plot(dates, completed_counts, marker="o", linestyle="-", color="blue", label="Daily Progress")
    plt.xlabel("Date")
    plt.ylabel("Habits Completed")
    plt.title("Habit Tracker Progress")
    plt.legend()
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()

# ✅ UI Setup (Tkinter)
root = tk.Tk()
root.title("Habit Tracker")
root.geometry("600x750")

# 🔹 Date Selection Dropdowns
date_frame = ttk.Frame(root)
date_frame.pack(pady=10)

ttk.Label(date_frame, text="Select Date:").grid(row=0, column=0, padx=5)

year_var = tk.StringVar(value=str(datetime.date.today().year))
month_var = tk.StringVar(value=f"{datetime.date.today().month:02d}")
day_var = tk.StringVar(value=f"{datetime.date.today().day:02d}")

year_dropdown = ttk.Combobox(date_frame, textvariable=year_var, values=[str(y) for y in range(2020, 2031)], width=5)
month_dropdown = ttk.Combobox(date_frame, textvariable=month_var, values=[f"{m:02d}" for m in range(1, 13)], width=3)
day_dropdown = ttk.Combobox(date_frame, textvariable=day_var, values=[f"{d:02d}" for d in range(1, 32)], width=3)

year_dropdown.grid(row=0, column=1, padx=5)
month_dropdown.grid(row=0, column=2, padx=5)
day_dropdown.grid(row=0, column=3, padx=5)

# 🔹 Habit Frame
ttk.Label(root, text="Daily, Weekly & Quarterly Habit Tracker", font=("Arial", 14, "bold")).pack(pady=10)
habit_frame = ttk.Frame(root)
habit_frame.pack(pady=10)
habit_vars = {}

# 🔹 Populate Habit List
def populate_habit_list():
    for widget in habit_frame.winfo_children():
        widget.destroy()

    habits = load_habits()
    if not habits:
        messagebox.showwarning("Warning", "No habits found!")

    last_category = None
    for habit_id, habit_name, category in habits:
        if category != last_category:
            ttk.Label(habit_frame, text=f"{category} Habits", font=("Arial", 12, "bold")).pack(anchor="w", pady=5)
            last_category = category

        var = tk.IntVar()
        habit_vars[habit_id] = var
        ttk.Checkbutton(habit_frame, text=habit_name, variable=var).pack(anchor="w", padx=20)

populate_habit_list()

# 🔹 Save & View Progress Buttons
ttk.Button(root, text="Save Progress", command=save_progress).pack(pady=10)
ttk.Button(root, text="View Progress", command=view_progress).pack(pady=10)

# 🔹 Footer: Designed by COSMY Consultancy
footer = tk.Label(root, text="Designed by COSMY Consultancy (with help of ChatGPT)", fg="blue", font=("Arial", 10, "italic"))
footer.pack(pady=20)

# ✅ Initialize Database & Load Data
init_db()
load_default_habits()
populate_habit_list()

root.mainloop()
