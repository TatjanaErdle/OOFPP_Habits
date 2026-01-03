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

def import_fixture():
    """
    Load initial demo data from test_fixture.sql if the database is empty.

    This function checks whether the habits table contains any rows.
    If it is empty, the SQL fixture is executed to populate the database
    with predefined demo habits and completion data. The fixture is only
    imported once and will not overwrite existing user data.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if habits table is empty
    cursor.execute("SELECT COUNT(*) FROM habits")
    count = cursor.fetchone()[0]

    if count == 0:
        with open("test_fixture.sql", "r") as f:
            sql_script = f.read()
        conn.executescript(sql_script)
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

def delete_habit(habit_id):
    """Deletes a habit and all its completions from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))
    cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))

    conn.commit()
    conn.close()

def edit_habit(habit_id, new_name=None, new_description=None, new_periodicity=None):
    """
    Update one or more fields of an existing habit.

    Only the fields provided as arguments are updated. Fields left as None
    remain unchanged.

    Args:
        habit_id (int): ID of the habit to update.
        new_name (str, optional): New name for the habit.
        new_description (str, optional): New description text.
        new_periodicity (str, optional): New periodicity ('daily', 'weekly', etc.).
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    if new_name:
        cursor.execute("UPDATE habits SET name=? WHERE id=?", (new_name, habit_id))
    if new_description:
        cursor.execute("UPDATE habits SET description=? WHERE id=?", (new_description, habit_id))
    if new_periodicity:
        cursor.execute("UPDATE habits SET periodicity=? WHERE id=?", (new_periodicity, habit_id))

    conn.commit()
    conn.close()

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
