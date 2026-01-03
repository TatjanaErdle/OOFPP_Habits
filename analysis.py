"""
analysis.py
-----------
This module provides analysis functions for the habit tracking system.
It enables the listing of all habits, filtering by periodicity, and
the calculation of streaks (longest series of completions) for individual
habits or across all habits.
"""

from db import get_habits, get_completions
from datetime import datetime

# --- List functions ---


def list_all_habits():
    """
    Returns a list of all habits stored in the database.
    """
    return get_habits()


def list_by_periodicity(periodicity):
    """
    Returns a list of all habits with a given periodicity (e.g. 'daily', 'weekly').
    """
    habits = get_habits()
    filtered = []

    for h in habits:
        if h[3] == periodicity:
            filtered.append(h)

    return filtered


# --- Streak analyses ---


def get_period_identifier(date, periodicity):
    """
    Convert a date into a comparable period identifier based on the habit's periodicity.

    This is used to determine whether two completion dates belong to consecutive
    periods (e.g., consecutive days, weeks, months, or years).

    Returns:
        A value representing the period:
        - daily: datetime.date
        - weekly: (year, ISO week number)
        - monthly: (year, month)
        - yearly: year (int)
    """

    if periodicity == "daily":
        return date
    elif periodicity == "weekly":
        iso = date.isocalendar()
        return iso[0], iso[1]
    elif periodicity == "monthly":
        return date.year, date.month
    elif periodicity == "yearly":
        return date.year
    return None


def get_longest_streak_for_habit(habit_id):
    """
    Calculates the longest historical streak for a habit,
    considering its periodicity.
    Returns None if habit not found.
    """
    habits = get_habits()
    row = next((h for h in habits if h[0] == habit_id), None)
    if row is None:
        return None

    periodicity = row[3].lower()
    completions = get_completions(habit_id)
    if not completions:
        return 0

    # Convert timestamps to date objects
    dates = sorted(
        datetime.strptime(c[0], "%Y-%m-%d %H:%M:%S").date() for c in completions
    )
    periods = [get_period_identifier(d, periodicity) for d in dates]
    unique_periods = sorted(set(periods))

    # Count longest consecutive streak
    longest = 1
    current = 1

    for i in range(1, len(unique_periods)):
        prev = unique_periods[i - 1]
        curr = unique_periods[i]

        if periodicity == "daily":
            if (curr - prev).days == 1:
                current += 1
            else:
                current = 1

        elif periodicity == "weekly":
            same_year = curr[0] == prev[0]
            next_week = curr[1] - prev[1] == 1
            year_rollover = curr[0] - prev[0] == 1 and prev[1] == 52 and curr[1] == 1

            if (same_year and next_week) or year_rollover:
                current += 1
            else:
                current = 1

        elif periodicity == "monthly":
            year_diff = curr[0] - prev[0]
            month_diff = curr[1] - prev[1]

            if (year_diff == 0 and month_diff == 1) or (
                year_diff == 1 and prev[1] == 12 and curr[1] == 1
            ):
                current += 1
            else:
                current = 1

        elif periodicity == "yearly":
            if curr - prev == 1:
                current += 1
            else:
                current = 1

        if current > longest:
            longest = current

    return longest


def get_longest_streak_all_habits():
    """
    Calculates the longest historical streak across all habits.
    Returns: longest_streak (int).
    """
    habits = get_habits()
    longest = 0

    for h in habits:
        streak = get_longest_streak_for_habit(h[0])
        if streak and streak > longest:
            longest = streak

    return longest
