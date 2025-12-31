# `TESTS.md`

# Habit Tracker - Test Documentation

This document describes the complete test coverage and testing strategy of the Habit Tracker project. 
The tests are organized into **Unit Tests**, **Functional Requirements Tests**, and **Integration Tests**, 
following a clear and maintainable test pyramid.

---

## Table of Contents

1. [Fixture Reset (Database Setup)](#fixture-reset-database-setup)
2. [monkeypatch (Unit Test Isolation)](#monkeypatch-unit-test-isolation)
3. [Test Stability with freezegun](#test-stability-with-freezegun)
4. [Tests](#tests)
   - [Unit Tests](#1-unit-tests-fast-isolated)
   - [Functional Requirements Tests](#2-functional-requirements-tests)
   - [Integration Tests](#3-integration-tests-db--sql-fixture)
   - [Main (CLI)](#4-main-mainpy)
   - [Test Pyramid](#5-test-pyramid)
5. [Summary](#summary)
6. [Test Execution Screenshots](#test-execution-screenshots)

---

## Fixture Reset (Database Setup) 

All integration tests use a `pytest` fixture that **recreates the test database (`test_habits.db`) before each test run**. 

The fixture performs the following steps: 

1. Deletes the existing `test_habits.db` file 
2. Creates a fresh database 
3. Builds the table structure 
4. Loads the static SQL fixture (`test_fixture.sql`) containing **4 weeks of predefined habit data** 
5. After each test, the database is removed again

This ensures: 
- deterministic test results 
- no cross‑test interference 
- reproducible behavior across all environments

---

## monkeypatch (Unit Test Isolation) 
In unit tests, the `pytest` fixture **monkeypatch** is used to temporarily replace functions or objects. 
This isolates logic from external dependencies such as the database. 

Examples: 

- Replacing `db.get_habits()` with a fake function 
- Replacing `sqlite3.connect()` with a `FakeConn` object 
- Returning controlled values to test logic only 

This ensures that unit tests verify **only the function under test**, without relying on real I/O or the database.

---

## Test Stability with freezegun 
Some features depend on the current date (e.g., streaks, due dates). 
To ensure deterministic results, the **freezegun** package is used to freeze time during tests. 

Example: 
```
@freeze_time("2025-11-16 12:00:00")
```

This guarantees:
- stable streak calculations 
- reproducible due‑date logic 
- independence from the actual system date

---

## Tests

### 1. Unit Tests (fast, isolated)
Unit tests validate pure logic without touching the real database.
They use monkeypatching and fake objects to isolate behavior.

#### Habit logic (habit.py)
- __init__ → object initialization 
- CRUD logic (creation, editing, deletion)
- is_completed_today 
- mark_completed (monkeypatched DB)
- get_streak (with frozen time)
- was_completed_this_period 
- is_due_today / is_overdue 
- next_due_date

#### Analytics module (analysis.py) 
- list_all_habits 
- list_by_periodicity 
- get_period_identifier (daily/weekly/monthly/yearly)
- get_longest_streak_for_habit 
- get_longest_streak_all_habits

These tests verify the functional programming paradigm:
pure functions, no side effects, no DB access.

#### HabitManager (unit-level)
- edit_habit (monkeypatched DB)
- delete_habit (monkeypatched DB)

### 2. Functional Requirements Tests
A dedicated test class verifies the explicit functional requirements from the assignment.
These tests do not focus on internal implementation, but on what the system must be able to do.

Covered Requirements

1. Habits can be created
2. Habits can be edited
3. Habits can be deleted
4. Habit completions can be recorded
5. All four analytics functions work
6. The 4‑week fixture supports correct streak calculations

These tests provide a direct mapping between the assignment and the implementation, 
making it easy for reviewers to verify correctness.

### 3. Integration Tests (DB + SQL Fixture)
Integration tests validate the interaction between modules using a real SQLite database 
populated with the 4‑week fixture.

#### Database (db.py)
- add_habit → new habit is stored correctly 
- get_habits → fixture integrity (5 habits)
- get_completions → correct number of entries (e.g., Meditation = 15)
- mark_completion → new completion entry is added

#### Habit (habit.py) with real data
- streak calculation (Reading = 28 days)
- due‑date logic 
- overdue logic 
- completion tracking

#### HabitManager (habitmanager.py)
- load_habits → loads all habits 
- get_habit_by_id 
- add_new_habit 
- delete_habit 
- complete_habit 
- get_habit_status (DONE / DUE / OVERDUE)
- get_habit_with_stats → correct structure and counts

#### Analytics (analysis.py) with real data
- list_all_habits → returns fixture habits 
- list_by_periodicity → correct filtering 
- get_longest_streak_for_habit → Reading = 28 
- get_longest_streak_all_habits → longest streak = 28

### 4. Main (main.py)
main.py contains only CLI logic (menus, input/output).
No separate tests are required because:
- all business logic is already tested in the modules 
- CLI testing would require interactive input mocking 
- the assignment does not require CLI tests

### 5. Test Pyramid

                ▲
                │
                │  End-to-End Tests (optional)
                │  – not required for this project
                │
        ┌───────────────────────────────────┐
        │         Integration Tests         │
        │───────────────────────────────────│
        │ - HabitManager + DB               │
        │ - db.py + SQL Fixture             │
        │ - Habit with real data            │
        │ - Analytics with fixture          │
        └───────────────────────────────────┘
                ▲
                │  tests interaction of modules
                │  + real 4‑week time-series data
                │
        ┌───────────────────────────────────┐
        │   Functional Requirements Tests   │
        │───────────────────────────────────│
        │ - Requirements 1–5                │
        └───────────────────────────────────┘
                ▲
                │
        ┌───────────────────────────────────┐
        │            Unit Tests             │
        │───────────────────────────────────│
        │ - Habit logic (CRUD)              │
        │ - Analytics (FP)                  │
        │ - monkeypatch instead of DB       │
        │ - FakeConn / FakeCursor           │
        └───────────────────────────────────┘
                ▲
                │  tests pure logic
                │  without external dependencies

---

## Summary
- Unit Tests → fast, isolated, functional programming verified 
- Functional Requirements Tests → assignment requirements explicitly validated
- Integration Tests → real DB + 4‑week fixture + module interaction
- freezegun ensures deterministic date‑dependent behavior 
- monkeypatch isolates logic from external dependencies

This structure ensures that the project is both technically correct and functionally complete, matching the expectations of the assignment.

---

## Test Execution Screenshots

### 1. All tests passing (`pytest -q`)
<img width="676" height="86" alt="image" src="https://github.com/user-attachments/assets/b084f934-e499-4fe4-882f-9dac8a412e2e" />

### 2. Functional Requirements Tests
<img width="827" height="72" alt="image" src="https://github.com/user-attachments/assets/ef244315-2f72-4e1c-871d-b5a072a78266" />

### 3. Integration Tests with SQL Fixture
<img width="838" height="67" alt="image" src="https://github.com/user-attachments/assets/8d3f73c4-44e9-414e-82cc-65e2167cf0ed" />





