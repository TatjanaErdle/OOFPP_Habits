"""
db.py
-----
This module contains all database operations for the habit tracking system.
It provides functions for creating tables, adding habits,
marking completions, and retrieving habits and their completions.
"""

import sqlite3
from datetime import datetime

DB_NAME = "habits.db"

# --- Setup / Connection ---

def get_db_connection():
    """Connects to the database and returns a connection object."""
    conn = sqlite3.connect(DB_NAME)
    return conn

def create_tables():
    """Creates tables for habits and completions if they don't already exist."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            periodicity TEXT,
            created_at TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS completions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            habit_id INTEGER,
            completed_at TEXT,
            FOREIGN KEY(habit_id) REFERENCES habits(id)
        )
    """)

    conn.commit()
    conn.close()

# --- Habits ---

def add_habit(name, description, periodicity):
    """Inserts a new habit into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO habits (name, description, periodicity, created_at) VALUES (?, ?, ?, ?)",
        (name, description, periodicity, created_at)
    )

    conn.commit()
    conn.close()

def get_habits():
    """Retrieves all habits from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM habits")
    habits = cursor.fetchall()

    conn.close()
    return habits

# --- Completions ---

def mark_completion(habit_id):
    """Marks a habit as completed by adding a timestamp to the completions table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    completed_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute(
        "INSERT INTO completions (habit_id, completed_at) VALUES (?, ?)",
        (habit_id, completed_at)
    )

    conn.commit()
    conn.close()

def get_completions(habit_id):
    """Retrieves all completion dates for a specific habit."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT completed_at FROM completions WHERE habit_id = ?", (habit_id,))
    completions = cursor.fetchall()

    conn.close()
    return completions
