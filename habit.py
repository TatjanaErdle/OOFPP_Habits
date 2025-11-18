"""
habit.py
--------
This module defines the Habit class, which represents a single habit.
It contains methods for managing completions (mark_completed, is_completed_today),
calculating streaks, checking due/overdue status, and determining the next due date.
"""

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import db
from db import mark_completion, get_completions


class Habit:
    """
    Represents a single habit with its attributes and related logic.
    """
    def __init__(self, habit_id, name, description, periodicity, created_at=None):
        self.id = habit_id  # avoid shadowing built-in "id"
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # --- Actions ---

    def mark_completed(self):
        """
        Adds a current timestamp if the habit has not yet been completed today.
        """
        if not self.is_completed_today():
            mark_completion(self.id)
            print(f"Habit '{self.name}' marked as completed.")
        else:
            print(f"Habit '{self.name}' was already completed today.")

    def is_completed_today(self):
        """
        Checks whether the habit has already been completed today.
        """
        completions = get_completions(self.id)
        today = datetime.now().date()
        return any(datetime.strptime(c[0], "%Y-%m-%d %H:%M:%S").date() == today for c in completions)

    # --- Help method ---

    @staticmethod
    def get_period_identifier(date, periodicity):
        """Returns a comparable period identifier for date depending on periodicity."""
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

    # --- Analysis ---

    def get_streak(self):
        """
        Calculates the streak for daily, weekly, monthly, and yearly habits.
        A streak continues only when consecutive periods contain a completion.
        """

        completions = db.get_completions(self.id)
        if not completions:
            return 0

        # Converts timestamps to date objects.
        dates = sorted(datetime.strptime(c[0], "%Y-%m-%d %H:%M:%S").date() for c in completions)

        periodicity = self.periodicity.lower()

        # Builds a list of all periods where the habit was completed.
        periods = [Habit.get_period_identifier(d, periodicity) for d in dates]

        # Removes duplicates → one mark per period is enough.
        unique_periods = sorted(list(set(periods)))

        # Determines the current period identifier.
        today = datetime.now().date()
        current_period = Habit.get_period_identifier(today, periodicity)

        if current_period not in unique_periods:
            return 0

        # Counts backwards.
        streak = 1
        index = unique_periods.index(current_period)

        for i in range(index, 0, -1):
            current = unique_periods[i]
            previous = unique_periods[i - 1]

            if periodicity == "daily":
                if (current - previous).days == 1:
                    streak += 1
                else:
                    break

            elif periodicity == "weekly":
                same_year = current[0] == previous[0]
                next_week = current[1] - previous[1] == 1
                year_rollover = current[0] - previous[0] == 1 and previous[1] == 52 and current[1] == 1

                if (same_year and next_week) or year_rollover:
                    streak += 1
                else:
                    break

            elif periodicity == "monthly":
                year_diff = current[0] - previous[0]
                month_diff = current[1] - previous[1]

                if (year_diff == 0 and month_diff == 1) or (year_diff == 1 and previous[1] == 12 and current[1] == 1):
                    streak += 1
                else:
                    break

            elif periodicity == "yearly":
                if current - previous == 1:
                    streak += 1
                else:
                    break

        return streak

    def was_completed_this_period(self):
        """Checks if the habit was completed in the current period."""
        completions = db.get_completions(self.id)
        if not completions:
            return False

        last_completion = max(
            datetime.strptime(c[0], "%Y-%m-%d %H:%M:%S") for c in completions
        ).date()

        today = datetime.now().date()

        if self.periodicity == "daily":
            return last_completion == today

        if self.periodicity == "weekly":
            start_of_week = today - timedelta(days=today.weekday())  # Monday
            end_of_week = start_of_week + timedelta(days=6)  # Sunday
            return start_of_week <= last_completion <= end_of_week

        if self.periodicity == "monthly":
            return last_completion.year == today.year and last_completion.month == today.month

        if self.periodicity == "yearly":
            return last_completion.year == today.year

        return False

    # --- Status ---

    def is_due_today(self):
        return not self.was_completed_this_period()

    def is_overdue(self):
        """
        Returns True if the habit was not completed in the most recent full period.
        For example:
        - daily: yesterday not completed
        - weekly: last week not completed
        - monthly: last month not completed
        - yearly: last year not completed
        """
        completions = db.get_completions(self.id)
        if not completions:
            return True

        last_completion = max(
            datetime.strptime(c[0], "%Y-%m-%d %H:%M:%S") for c in completions
        ).date()
        today = datetime.now().date()

        if self.periodicity == "daily":
            yesterday = today - timedelta(days=1)
            return last_completion < yesterday

        if self.periodicity == "weekly":
            # Last week: Monday to Sunday of the previous week
            start_of_last_week = today - timedelta(days=today.weekday() + 7)
            end_of_last_week = start_of_last_week + timedelta(days=6)
            return not (start_of_last_week <= last_completion <= end_of_last_week)

        if self.periodicity == "monthly":
            # Last month
            if today.month == 1:
                last_month = 12
                year = today.year - 1
            else:
                last_month = today.month - 1
                year = today.year
            return (last_completion.year, last_completion.month) < (year, last_month)

        if self.periodicity == "yearly":
            last_year = today.year - 1
            return last_completion.year < last_year

        return False

    # --- Planning ---

    def next_due_date(self):
        completions = db.get_completions(self.id)

        if not completions:
            return datetime.now().date()

        parsed_dates = []
        for c in completions:
            try:
                parsed_dates.append(datetime.strptime(c[0], "%Y-%m-%d %H:%M:%S"))
            except ValueError:
                parsed_dates.append(datetime.fromisoformat(c[0]))

        last = max(parsed_dates).date()

        if self.periodicity == "daily":
            return last + timedelta(days=1)

        elif self.periodicity == "weekly":
            return last + timedelta(weeks=1)

        elif self.periodicity == "monthly":
            return last + relativedelta(months=1)

        elif self.periodicity == "yearly":
            return last + relativedelta(years=1)

        return None

