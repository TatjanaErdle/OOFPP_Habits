"""
test_project.py
-------
This file contains automated tests for all core modules:
- db.py (database functions)
- habit.py (habit logic)
- habitManager.py (management and output)
- analysis.py (evaluations and streaks)
The tests access the separate test database 'test_habits.db',
which is populated reproducibly via an SQL fixture.

Note:
For habits that depend on the current date (e.g., streaks, due date),
the **freezegun** package is used.
This freezes the date in the test run (e.g., on November 16, 2025).
This ensures stable results, independent of the actual day the tests are run.
"""

import os
import sqlite3
import pytest
import db
import analysis
from habit import Habit
import datetime
from habitmanager import HabitManager
from freezegun import freeze_time


# Use test database
db.DB_NAME = "test_habits.db"
TEST_DB = db.DB_NAME

@pytest.fixture(autouse=True)
def setup_db():
    # Before each test: Create a new database
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    conn = sqlite3.connect(TEST_DB)

    # Create table structure
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        periodicity TEXT,
        created_at TEXT
    );
    CREATE TABLE IF NOT EXISTS completions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        habit_id INTEGER,
        completed_at TEXT,
        FOREIGN KEY(habit_id) REFERENCES habits(id)
    );
    """)

    # Import fixture data
    with open("test_fixture.sql", "r") as f:
        sql_script = f.read()
    conn.executescript(sql_script)
    conn.commit()
    conn.close()

    yield  # Tests are running here

    # After each test: Delete database
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

# --- Tests for db.py ---

def test_add_habit_and_get_habits():
    # Add new habit
    from db import add_habit, get_habits
    add_habit("Testing habit", "Test", "daily")
    habits = get_habits()
    names = [h[1] for h in habits]
    assert "Testing habit" in names

def test_get_habits_fixture_integrity():
    from db import get_habits
    habits = get_habits()
    assert len(habits) == 5  # Fixture contains 5 habits

def test_get_completions_fixture_meditation():
    from db import get_habits, get_completions
    habits = get_habits()
    meditation_id = [h[0] for h in habits if h[1] == "Meditation"][0]
    completions = get_completions(meditation_id)
    assert len(completions) == 15  # according to the fixture

def test_mark_completion_adds_entry():
    from db import get_habits, get_completions, mark_completion
    habits = get_habits()
    habit_id = habits[0][0]
    before = len(get_completions(habit_id))
    mark_completion(habit_id)
    after = len(get_completions(habit_id))
    assert after == before + 1

# --- Tests for habit.py ---

def test_habit_object_initialization():
    habits = db.get_habits()
    h = habits[0]
    habit = Habit(h[0], h[1], h[2], h[3])
    assert habit.name == h[1]
    assert habit.periodicity in ["daily", "weekly", "monthly", "yearly"]

def test_is_completed_today_false_for_old_habit():
    habits = db.get_habits()
    meditation = [h for h in habits if h[1] == "Meditation"][0]
    habit = Habit(meditation[0], meditation[1], meditation[2], meditation[3])
    assert habit.is_completed_today() is False  # Fixture contains no entries for today

def test_mark_completed_adds_today_entry():
    habits = db.get_habits()
    meditation = [h for h in habits if h[1] == "Meditation"][0]
    habit = Habit(meditation[0], meditation[1], meditation[2], meditation[3])
    before = len(db.get_completions(habit.id))
    habit.mark_completed()
    after = len(db.get_completions(habit.id))
    assert after == before + 1

@freeze_time("2025-11-16 12:00:00")
def test_get_streak_for_reading():
    habits = db.get_habits()
    reading = [h for h in habits if h[1] == "Reading"][0]
    habit = Habit(reading[0], reading[1], reading[2], reading[3])
    assert habit.get_streak() == 28

@freeze_time("2025-11-16 12:00:00")
def test_was_completed_this_period_true_for_reading():
    habits = db.get_habits()
    reading = [h for h in habits if h[1] == "Reading"][0]
    habit = Habit(reading[0], reading[1], reading[2], reading[3])
    assert habit.was_completed_this_period() is True

@freeze_time("2025-11-16 12:00:00")
def test_is_due_today_false_for_reading():
    habits = db.get_habits()
    reading = [h for h in habits if h[1] == "Reading"][0]
    habit = Habit(reading[0], reading[1], reading[2], reading[3])
    assert habit.is_due_today() is False

def test_is_overdue_true_for_meditation():
    habits = db.get_habits()
    meditation = [h for h in habits if h[1] == "Meditation"][0]
    habit = Habit(meditation[0], meditation[1], meditation[2], meditation[3])
    assert habit.is_overdue() is True

@freeze_time("2025-11-16 12:00:00")
def test_next_due_date_for_reading():
    habits = db.get_habits()
    reading = [h for h in habits if h[1] == "Reading"][0]
    habit = Habit(reading[0], reading[1], reading[2], reading[3])
    next_due = habit.next_due_date()
    assert next_due > datetime.date(2025, 11, 16)

# --- Tests for habitmanager.py ---

def test_manager_loads_all_habits():
    manager = HabitManager()
    manager.load_habits()
    habits = manager.get_all_habits()
    assert len(habits) == 5
    assert all(hasattr(h, "name") for h in habits)

def test_manager_get_habit_by_id():
    manager = HabitManager()
    manager.load_habits()
    first_id = manager.get_all_habits()[0].id
    habit = manager.get_habit_by_id(first_id)
    assert habit is not None
    assert habit.id == first_id

def test_manager_add_and_delete_habit():
    manager = HabitManager()
    manager.load_habits()
    initial_count = len(manager.get_all_habits())
    manager.add_new_habit("Temp Habit", "To be deleted", "daily")
    updated_count = len(manager.get_all_habits())
    assert updated_count == initial_count + 1
    temp_habit = [h for h in manager.get_all_habits() if h.name == "Temp Habit"][0]
    manager.delete_habit(temp_habit.id)
    final_count = len(manager.get_all_habits())
    assert final_count == initial_count

def test_manager_complete_habit_adds_entry():
    manager = HabitManager()
    manager.load_habits()
    habit = manager.get_all_habits()[0]
    before = len(db.get_completions(habit.id))
    manager.complete_habit(habit.id)
    after = len(db.get_completions(habit.id))
    assert after == before + 1

def test_manager_get_habit_status_returns_valid_string():
    manager = HabitManager()
    manager.load_habits()
    habit = manager.get_all_habits()[0]
    status = manager.get_habit_status(habit)
    assert status in ["DONE", "DUE", "OVERDUE"]

def test_manager_get_habit_with_stats_structure():
    manager = HabitManager()
    manager.load_habits()
    stats = manager.get_habit_with_stats()
    assert isinstance(stats, list)
    assert all("completions" in h for h in stats)
    assert all(isinstance(h["completions"], int) for h in stats)

# --- Tests for analysis.py ---

def test_list_all_habits_returns_fixture():
    habits = analysis.list_all_habits()
    assert isinstance(habits, list)
    assert len(habits) == 5  # according to the fixture

def test_list_by_periodicity_daily():
    daily_habits = analysis.list_by_periodicity("daily")
    assert isinstance(daily_habits, list)
    assert all(h[3] == "daily" for h in daily_habits)
    assert any(h[1] == "Reading" for h in daily_habits)

def test_list_by_periodicity_weekly():
    weekly_habits = analysis.list_by_periodicity("weekly")
    assert isinstance(weekly_habits, list)
    assert all(h[3] == "weekly" for h in weekly_habits)
    assert any(h[1] == "Jogging" for h in weekly_habits)

def test_get_longest_streak_for_reading():
    habits = db.get_habits()
    reading_id = [h[0] for h in habits if h[1] == "Reading"][0]
    streak = analysis.get_longest_streak_for_habit(reading_id)
    assert streak == 28  # according to the fixture

def test_get_longest_streak_for_meditation():
    habits = db.get_habits()
    meditation_id = [h[0] for h in habits if h[1] == "Meditation"][0]
    streak = analysis.get_longest_streak_for_habit(meditation_id)
    assert streak < 28  # Meditation has gaps

def test_get_longest_streak_all_habits():
    longest = analysis.get_longest_streak_all_habits()
    assert longest == 28  # Reading has the longest streak

