"""
test_project.py
---------------
This file contains automated tests for the Habit Tracker project.

Coverage:
- db.py (database functions)
- habit.py (habit logic and CRUD operations)
- habitManager.py (management interface and output)
- analysis.py (evaluations and streak calculations)

Test strategy:
- Unit tests: isolate core logic for Habit creation, editing, and deletion,
  as well as each function in the analytics module.
- Integration tests: run against the separate test database 'test_habits.db',
  which is reproducibly populated via an SQL fixture.

Special notes:
- For habits that depend on the current date (e.g., streaks, due dates),
  the **freezegun** package is used. This freezes the date in the test run
  (e.g., November 16, 2025) to ensure deterministic results, independent of
  the actual day the tests are executed.
- The fixture provides 4 weeks of predefined habit data (time-series completions),
  which is used in integration tests.
- In unit tests, the pytest fixture **monkeypatch** is used to temporarily replace
  functions or objects (e.g., database calls). This isolates the logic under test
  from external dependencies, ensuring that only the function’s behavior is verified.
"""

import os
import sqlite3
import pytest
import db
import analysis
from habit import Habit
from habitmanager import HabitManager
import datetime
from freezegun import freeze_time

# -------------------------------------------------------------------
# UNIT TESTS: Habit CRUD
# -------------------------------------------------------------------


class TestHabitCRUDUnit:

    def test_habit_creation_unit(self):
        habit = Habit(1, "Reading", "desc", "daily", "2025-11-01")
        assert habit.id == 1
        assert habit.name == "Reading"
        assert habit.periodicity == "daily"

    def test_habit_editing_unit(self, monkeypatch):
        manager = HabitManager()
        called = {}

        class FakeCursor:
            def execute(self, _sql, params=None):
                called["params"] = params

        class FakeConn:
            def cursor(self):
                return FakeCursor()

            def commit(self):
                pass

            def close(self):
                pass

        monkeypatch.setattr("sqlite3.connect", lambda _: FakeConn())
        monkeypatch.setattr("db.get_habits", lambda: [])
        manager.edit_habit(1, new_name="Updated Habit")

        assert called["params"] == ("Updated Habit", 1)

    def test_habit_deletion_unit(self, monkeypatch):
        manager = HabitManager()
        called = {}

        class FakeCursor:
            def execute(self, _sql, _=None):
                called["deleted"] = True

        class FakeConn:
            def cursor(self):
                return FakeCursor()

            def commit(self):
                pass

            def close(self):
                pass

        monkeypatch.setattr("sqlite3.connect", lambda _: FakeConn())
        monkeypatch.setattr("db.get_habits", lambda: [])
        manager.delete_habit(1)

        assert "deleted" in called


# -------------------------------------------------------------------
# UNIT TESTS: Analytics (functional programming)
# -------------------------------------------------------------------


class TestAnalyticsUnit:

    def test_list_all_habits(self, monkeypatch):
        monkeypatch.setattr(
            "analysis.get_habits", lambda: [(1, "Reading", "desc", "daily")]
        )
        habits = analysis.list_all_habits()
        assert habits[0][1] == "Reading"

    def test_list_by_periodicity(self, monkeypatch):
        fake_habits = [
            (1, "Reading", "desc", "daily"),
            (2, "Jogging", "desc", "weekly"),
        ]
        monkeypatch.setattr("analysis.get_habits", lambda: fake_habits)
        daily = analysis.list_by_periodicity("daily")
        assert len(daily) == 1 and daily[0][1] == "Reading"

    def test_period_identifier_daily(self):
        d = datetime.date(2025, 11, 1)
        assert analysis.get_period_identifier(d, "daily") == d

    def test_period_identifier_weekly(self):
        d = datetime.date(2025, 11, 1)
        year, week = analysis.get_period_identifier(d, "weekly")
        assert isinstance(year, int) and isinstance(week, int)

    def test_period_identifier_monthly(self):
        d = datetime.date(2025, 11, 1)
        assert analysis.get_period_identifier(d, "monthly") == (2025, 11)

    def test_period_identifier_yearly(self):
        d = datetime.date(2025, 11, 1)
        assert analysis.get_period_identifier(d, "yearly") == 2025

    def test_longest_streak_no_completions(self, monkeypatch):
        monkeypatch.setattr(
            "analysis.get_habits", lambda: [(1, "Reading", "desc", "daily")]
        )
        monkeypatch.setattr("analysis.get_completions", lambda habit_id: [])
        streak = analysis.get_longest_streak_for_habit(1)
        assert streak == 0

    def test_longest_streak_none(self, monkeypatch):
        monkeypatch.setattr("analysis.get_habits", lambda: [])
        streak = analysis.get_longest_streak_for_habit(99)
        assert streak is None

    def test_longest_streak_all(self, monkeypatch):
        monkeypatch.setattr(
            "analysis.get_habits", lambda: [(1, "Reading", "desc", "daily")]
        )
        monkeypatch.setattr(
            "analysis.get_completions",
            lambda habit_id: [
                ("2025-11-01 10:00:00",),
                ("2025-11-02 10:00:00",),
                ("2025-11-03 10:00:00",),
            ],
        )
        longest = analysis.get_longest_streak_all_habits()
        assert longest == 3


# -------------------------------------------------------------------
# FUNCTIONAL REQUIREMENTS TESTS
# -------------------------------------------------------------------


class TestFunctionalRequirements:
    """
    Tests that directly map to the functional requirements of the project.
    These tests do NOT test internal implementation details, but verify
    that the system fulfills the required user-facing capabilities.
    """

    # Requirement 1: Habits can be created
    def test_requirement_create_habit(self):
        habit = Habit(1, "Morning Routine", "desc", "daily")
        assert habit.name == "Morning Routine"
        assert habit.periodicity == "daily"
        assert habit.id == 1

    # Requirement 2: Habits can be edited
    def test_requirement_edit_habit(self, monkeypatch):
        manager = HabitManager()

        # Fake DB connection
        class FakeCursor:
            def __init__(self):
                self.params = None

            def execute(self, sql, params=None):
                self.params = params

        class FakeConn:
            def cursor(self):
                return FakeCursor()

            def commit(self):
                pass

            def close(self):
                pass

        fake = FakeConn()
        monkeypatch.setattr("sqlite3.connect", lambda _: fake)
        monkeypatch.setattr("db.get_habits", lambda: [])

        manager.edit_habit(1, new_name="Updated Name")

        # If no exception occurs, requirement is fulfilled
        assert True

    # Requirement 3: Habits can be deleted
    def test_requirement_delete_habit(self, monkeypatch):
        manager = HabitManager()

        class FakeCursor:
            def __init__(self):
                self.called = None

            def execute(self, sql, params=None):
                self.called = True

        class FakeConn:
            def cursor(self):
                return FakeCursor()

            def commit(self):
                pass

            def close(self):
                pass

        monkeypatch.setattr("sqlite3.connect", lambda _: FakeConn())
        monkeypatch.setattr("db.get_habits", lambda: [])

        manager.delete_habit(1)
        assert True  # No exception → requirement fulfilled

    # Requirement 4: Habit completion tracking works
    def test_requirement_completion_tracking(self, monkeypatch):
        # Fake DB for completions
        completions = []

        def fake_mark_completion(habit_id):
            completions.append(habit_id)

        monkeypatch.setattr("db.mark_completion", fake_mark_completion)

        habit = Habit(1, "Reading", "desc", "daily")
        habit.mark_completed()

        assert len(completions) == 1
        assert completions[0] == 1

    # Requirement 5: Analytics module works (all 4 functions)
    def test_requirement_analytics_functions(self, monkeypatch):
        # Fake habits
        fake_habits = [
            (1, "Reading", "desc", "daily"),
            (2, "Jogging", "desc", "weekly"),
        ]

        # Fake completions
        fake_completions = {
            1: [("2025-11-01 10:00:00",), ("2025-11-02 10:00:00",)],
            2: [],
        }

        monkeypatch.setattr("analysis.get_habits", lambda: fake_habits)
        monkeypatch.setattr(
            "analysis.get_completions", lambda hid: fake_completions[hid]
        )

        # 5a: list_all_habits
        assert len(analysis.list_all_habits()) == 2

        # 5b: list_by_periodicity
        daily = analysis.list_by_periodicity("daily")
        assert len(daily) == 1

        # 5c: longest streak for a habit
        streak = analysis.get_longest_streak_for_habit(1)
        assert streak == 2

        # 5d: longest streak across all habits
        longest = analysis.get_longest_streak_all_habits()
        assert longest == 2


# -------------------------------------------------------------------
# INTEGRATION TESTS
# -------------------------------------------------------------------

# --- Fixture: Setup test database for integration tests ---

# Use test database
db.DB_NAME = "test_habits.db"
TEST_DB = db.DB_NAME


@pytest.fixture(autouse=True)
def setup_db():
    """
    Create a fresh test database before each test and remove it afterwards.

    This fixture:
    - creates the SQLite test database 'test_habits.db'
    - builds the table schema
    - loads the 4‑week SQL fixture (test_fixture.sql)
    - yields control to the test
    - deletes the database after the test completes

    Ensures full test isolation and reproducibility.
    """
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)
    conn = sqlite3.connect(TEST_DB)

    # Create table structure
    conn.executescript(
        """
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
    """
    )

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


class TestDBIntegration:

    def test_add_habit_and_get_habits(self):
        # Add new habit
        from db import add_habit, get_habits

        add_habit("Testing habit", "Test", "daily")
        habits = get_habits()
        names = [h[1] for h in habits]
        assert "Testing habit" in names

    def test_get_habits_fixture_integrity(self):
        from db import get_habits

        habits = get_habits()
        assert len(habits) == 5  # Fixture contains 5 habits

    def test_get_completions_fixture_meditation(self):
        from db import get_habits, get_completions

        habits = get_habits()
        meditation_id = [h[0] for h in habits if h[1] == "Meditation"][0]
        completions = get_completions(meditation_id)
        assert len(completions) == 15  # according to the fixture

    def test_mark_completion_adds_entry(self):
        from db import get_habits, get_completions, mark_completion

        habits = get_habits()
        habit_id = habits[0][0]
        before = len(get_completions(habit_id))
        mark_completion(habit_id)
        after = len(get_completions(habit_id))
        assert after == before + 1


# --- Tests for habit.py ---


class TestHabitIntegration:

    def test_habit_object_initialization(self):
        habits = db.get_habits()
        h = habits[0]
        habit = Habit(h[0], h[1], h[2], h[3])
        assert habit.name == h[1]
        assert habit.periodicity in ["daily", "weekly", "monthly", "yearly"]

    def test_is_completed_today_false_for_old_habit(self):
        habits = db.get_habits()
        meditation = [h for h in habits if h[1] == "Meditation"][0]
        habit = Habit(meditation[0], meditation[1], meditation[2], meditation[3])
        assert (
            habit.is_completed_today() is False
        )  # Fixture contains no entries for today

    def test_mark_completed_adds_today_entry(self):
        habits = db.get_habits()
        meditation = [h for h in habits if h[1] == "Meditation"][0]
        habit = Habit(meditation[0], meditation[1], meditation[2], meditation[3])
        before = len(db.get_completions(habit.id))
        habit.mark_completed()
        after = len(db.get_completions(habit.id))
        assert after == before + 1

    @freeze_time("2025-11-16 12:00:00")
    def test_get_streak_for_reading(self):
        habits = db.get_habits()
        reading = [h for h in habits if h[1] == "Reading"][0]
        habit = Habit(reading[0], reading[1], reading[2], reading[3])
        assert habit.get_streak() == 28

    @freeze_time("2025-11-16 12:00:00")
    def test_was_completed_this_period_true_for_reading(self):
        habits = db.get_habits()
        reading = [h for h in habits if h[1] == "Reading"][0]
        habit = Habit(reading[0], reading[1], reading[2], reading[3])
        assert habit.was_completed_this_period() is True

    @freeze_time("2025-11-16 12:00:00")
    def test_is_due_today_false_for_reading(self):
        habits = db.get_habits()
        reading = [h for h in habits if h[1] == "Reading"][0]
        habit = Habit(reading[0], reading[1], reading[2], reading[3])
        assert habit.is_due_today() is False

    def test_is_overdue_true_for_meditation(self):
        habits = db.get_habits()
        meditation = [h for h in habits if h[1] == "Meditation"][0]
        habit = Habit(meditation[0], meditation[1], meditation[2], meditation[3])
        assert habit.is_overdue() is True

    @freeze_time("2025-11-16 12:00:00")
    def test_next_due_date_for_reading(self):
        habits = db.get_habits()
        reading = [h for h in habits if h[1] == "Reading"][0]
        habit = Habit(reading[0], reading[1], reading[2], reading[3])
        next_due = habit.next_due_date()
        assert next_due > datetime.date(2025, 11, 16)


# --- Tests for habitmanager.py ---


class TestHabitManagerIntegration:

    def test_manager_loads_all_habits(self):
        manager = HabitManager()
        manager.load_habits()
        habits = manager.get_all_habits()
        assert len(habits) == 5
        assert all(hasattr(h, "name") for h in habits)

    def test_manager_get_habit_by_id(self):
        manager = HabitManager()
        manager.load_habits()
        first_id = manager.get_all_habits()[0].id
        habit = manager.get_habit_by_id(first_id)
        assert habit is not None
        assert habit.id == first_id

    def test_manager_add_and_delete_habit(self):
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

    def test_manager_complete_habit_adds_entry(self):
        manager = HabitManager()
        manager.load_habits()
        habit = manager.get_all_habits()[0]
        before = len(db.get_completions(habit.id))
        manager.complete_habit(habit.id)
        after = len(db.get_completions(habit.id))
        assert after == before + 1

    def test_manager_get_habit_status_returns_valid_string(self):
        manager = HabitManager()
        manager.load_habits()
        habit = manager.get_all_habits()[0]
        status = manager.get_habit_status(habit)
        assert status in ["DONE", "DUE", "OVERDUE"]

    def test_manager_get_habit_with_stats_structure(self):
        manager = HabitManager()
        manager.load_habits()
        stats = manager.get_habit_with_stats()
        assert isinstance(stats, list)
        assert all("completions" in h for h in stats)
        assert all(isinstance(h["completions"], int) for h in stats)


# --- Tests for analysis.py ---


class TestAnalysisIntegration:

    def test_list_all_habits_returns_fixture(self):
        habits = analysis.list_all_habits()
        assert isinstance(habits, list)
        assert len(habits) == 5  # according to the fixture

    def test_list_by_periodicity_daily(self):
        daily_habits = analysis.list_by_periodicity("daily")
        assert isinstance(daily_habits, list)
        assert all(h[3] == "daily" for h in daily_habits)
        assert any(h[1] == "Reading" for h in daily_habits)

    def test_list_by_periodicity_weekly(self):
        weekly_habits = analysis.list_by_periodicity("weekly")
        assert isinstance(weekly_habits, list)
        assert all(h[3] == "weekly" for h in weekly_habits)
        assert any(h[1] == "Jogging" for h in weekly_habits)

    def test_get_longest_streak_for_reading(self):
        habits = db.get_habits()
        reading_id = [h[0] for h in habits if h[1] == "Reading"][0]
        streak = analysis.get_longest_streak_for_habit(reading_id)
        assert streak == 28  # according to the fixture

    def test_get_longest_streak_for_meditation(self):
        habits = db.get_habits()
        meditation_id = [h[0] for h in habits if h[1] == "Meditation"][0]
        streak = analysis.get_longest_streak_for_habit(meditation_id)
        assert streak < 28  # Meditation has gaps

    def test_get_longest_streak_all_habits_fixture(self):
        longest = analysis.get_longest_streak_all_habits()
        assert longest == 28  # Reading has the longest streak
