# `TESTS.md`

# Habit Tracker test documentation

This file describes the project's test coverage.

### Fixture Reset
All tests use a `pytest` fixture, which recreates the test database (`test_habits.db`) before each test run.

This process deletes the existing file, creates the table structure, and loads the static SQL fixture (`test_fixture.sql`).

After each test, the database is removed again.

This ensures that each test starts with a fresh, reproducible baseline, regardless of previous changes.

This way, the results are stable and the tests do not interfere with each other.

### Test Stability
For habits that depend on the current date (e.g., streaks, due date), 
the **freezegun** package is used. 
This freezes the date in the test run (e.g., on November 16, 2025). 
This ensures stable results, independent of the actual day the tests are run.

## Database (db.py)
- add_habit → checks if the new habit is saved correctly
- get_habits → checks fixture integrity (5 habits)
- mark_completion → checks if the completion entry is added
- get_completions → checks if all entries for meditation are returned

## Habit (habit.py)
- __init__ → checks object initialization
- is_completed_today → checks today's completion
- mark_completed → checks today's entry added
- get_streak → checks streak calculation (read = 28 days)
- was_completed_this_period → checks period completion
- is_due_today / is_overdue → checks due date and overdue date
- next_due_date → checks next due date calculation

## HabitManager (habitmanager.py)
- load_habits → checks that all habits are loaded
- get_habit_by_id → checks access by ID
- add_new_habit → checks adding new habits
- complete_habit → checks completion entry
- get_habit_status → checks status output (DONE/DUE/OVERDUE)
- get_habit_with_stats → checks statistics structure

## Analysis (analysis.py)
- list_all_habits → checks the return of all habits
- list_by_periodicity → checks filtering by frequency
- get_longest_streak_for_habit → checks the longest streak per habit
- get_longest_streak_all_habits → checks the longest streak in the system (28 days)

## Main (main.py)
- Contains only CLI logic (menus, input/output).
- No separate tests are required, as all modules are already covered.



<img width="782" height="65" alt="image" src="https://github.com/user-attachments/assets/5e1c98c8-eca8-4b6f-98ec-af5219d7e897" />

