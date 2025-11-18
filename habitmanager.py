"""
habitManager.py
----------------
This module contains the HabitManager class, which acts as an interface between
the command line interface (CLI) and the database. It manages
all habits, provides CRUD operations, marks completions, calculates status
and streaks, and provides output functions via rich tables.
"""

import sqlite3
from habit import Habit
from rich.table import Table
from rich.console import Console
import db



class HabitManager:
    """HabitManager is responsible for managing all habits
    and acts as the interface between the CLI and the database"""

    # --- Initialization & Setup ---

    def __init__(self):
        self.habits = []

    def initialize_database(self):
        """Ensures that the database tables exist."""
        db.create_tables()
        print("Database initialized or already existing.")

    # --- Load & Access ---

    def load_habits(self):
        """Loads all habits from the database into the list self.habits."""
        self.habits = []
        for row in db.get_habits():
            habit = Habit(
                habit_id=row[0],
                name=row[1],
                description=row[2],
                periodicity=row[3],
                created_at=row[4]
            )
            self.habits.append(habit)

    def get_all_habits(self):
        """Returns a list of all loaded Habit objects."""
        return self.habits

    def get_habit_by_id(self, habit_id):
        """Finds a Habit object based on its ID."""
        for habit in self.habits:
            if habit.id == habit_id:
                return habit
        return None

    # --- CRUD operations ---

    def add_new_habit(self, name, description, periodicity):
        """Creates a new habit and saves it in the database."""
        db.add_habit(name, description, periodicity)
        self.load_habits()  # then update list

    def delete_habit(self, habit_id):
        """Deletes a habit (and its completions) from the database."""
        conn = sqlite3.connect(db.DB_NAME)
        cursor = conn.cursor()

        cursor.execute("DELETE FROM completions WHERE habit_id = ?", (habit_id,))
        cursor.execute("DELETE FROM habits WHERE id = ?", (habit_id,))

        conn.commit()
        conn.close()
        print(f"Habit with ID {habit_id} deleted.")
        self.load_habits()

    # --- Completions ---

    def complete_habit(self, habit_id):
        db.mark_completion(habit_id)
        self.load_habits()

    # --- Status & Statistics ---

    def get_habit_status(self, habit):
        """Returns a readable status string for a habit."""
        if habit.was_completed_this_period():
            return "DONE"
        elif habit.is_overdue():
            return "OVERDUE"
        else:
            return "DUE"

    def get_habit_with_stats(self):
        """
        Returns habit data PLUS completion count.
        Useful for a table.
        """
        data = []
        for habit in self.habits:
            count = len(db.get_completions(habit.id))
            data.append({
                "id": habit.id,
                "name": habit.name,
                "description": habit.description,
                "periodicity": habit.periodicity,
                "created_at": habit.created_at,
                "completions": count
            })
        return data

    # --- Output (Rich Table) ---

    def _render_habits_table(self, habits, title="Habit Overview"):
        console = Console()
        table = Table(title=title)

        table.add_column("ID", justify="right")
        table.add_column("Name")
        table.add_column("Description")
        table.add_column("Periodicity")
        table.add_column("Streak", justify="center")
        table.add_column("Status", justify="center")
        table.add_column("Created At", justify="center")
        table.add_column("Last Completion", justify="center")

        for habit in habits:
            completions = db.get_completions(habit.id)
            last_completion = completions[-1][0] if completions else "-"
            status = self.get_habit_status(habit)

            status_colors = {
                "DONE": "[green]DONE[/green]",
                "OVERDUE": "[red]OVERDUE[/red]",
                "DUE": "[yellow]DUE[/yellow]"
            }
            status_colored = status_colors.get(status, "[yellow]DUE[/yellow]")

            desc = habit.description if len(habit.description) < 40 else habit.description[:37] + "..."

            table.add_row(
                str(habit.id),
                habit.name,
                desc,
                habit.periodicity,
                str(habit.get_streak()),
                status_colored,
                habit.created_at,
                last_completion,
        )

        console.print(table)

    def show_habits_rich(self):
        """Displays all habits from the database."""
        self.load_habits()
        habits = self.get_all_habits()
        self._render_habits_table(habits, title="Habit Overview")

    def show_habits_rich_for(self, habits, title="Habit Overview"):
        """Displays a list of habits that have been passed on."""
        self._render_habits_table(habits, title=title)


