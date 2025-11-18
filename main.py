"""
main.py
-------
This module launches the command line interface (CLI) for the habit tracking system.
It provides a main menu and submenus for habit-specific actions and analyses.
The HabitManager class is used as the central interface to the database.
"""

from habitmanager import HabitManager
import analysis
from rich.console import Console

console = Console()

# --- Setup / Getting Started ---

def main():
    """Starts the CLI for the Habit Tracker System."""
    manager = HabitManager()
    manager.initialize_database()
    manager.load_habits()

    while True:
        console.print("\n[bold cyan]===== HABIT TRACKER =====[/bold cyan]")
        print("1. Habit-specific actions")
        print("2. Show all habits")
        print("3. Analysis")
        print("4. Exit")

        choice = input("Please select an option (1–4): ")

        if choice == "1":
            show_habit_actions_menu(manager)

        elif choice == "2":
            manager.show_habits_rich()

        elif choice == "3":
            show_analysis_menu(manager)

        elif choice == "4":
            console.print("[bold cyan]Program is ending. Goodbye![/bold cyan]")
            break

        else:
            console.print("[red]Invalid entry. Please select 1–4.[/red]")

# --- Habit-specific menu ---

def show_habit_actions_menu(manager):
    """Submenu for habit-specific actions."""
    while True:
        console.print("\n[bold yellow]--- Habit Actions ---[/bold yellow]")
        print("1. Create new habit")
        print("2. Delete habit")
        print("3. Mark habit as completed")
        print("4. Show current streak of a habit")
        print("5. Check if habit is completed today")
        print("6. Show next due date of a habit")
        print("7. Back to main menu")

        choice = input("Please select an option (1–7): ")

        if choice == "1":
            name = input("Enter habit name: ")
            description = input("Enter description: ")
            periodicity = input("Enter frequency (daily/weekly/monthly/yearly): ")
            manager.add_new_habit(name, description, periodicity)
            console.print(f"[green]Habit '{name}' created.[/green]")

        elif choice == "1":
            name = input("Enter habit name: ")
            description = input("Enter description: ")
            periodicity = input("Enter frequency (daily/weekly/monthly/yearly): ")

            # # Check for duplicate names
            existing_names = [h.name for h in manager.get_all_habits()]
            if name in existing_names:
                console.print(f"[red]Habit with name '{name}' already exists.[/red]")
            else:
                manager.add_new_habit(name, description, periodicity)
                console.print(f"[green]Habit '{name}' created.[/green]")

        elif choice == "2":
            manager.show_habits_rich()
            try:
                habit_id = int(input("Enter the ID of the habit to delete: "))
                habit = manager.get_habit_by_id(habit_id)
                if habit:
                    manager.delete_habit(habit_id)
                    console.print(f"[red]Habit {habit_id} deleted.[/red]")
                else:
                    console.print(f"[red]Habit with ID {habit_id} not found.[/red]")
            except ValueError:
                console.print("[red]Invalid input.[/red]")

        elif choice == "3":
            manager.show_habits_rich()
            try:
                habit_id = int(input("Enter the ID of the habit: "))
                habit = manager.get_habit_by_id(habit_id)
                if habit:
                    habit.mark_completed()
                else:
                    console.print(f"[red]Habit with ID {habit_id} not found.[/red]")
            except ValueError:
                console.print("[red]Invalid input.[/red]")

        elif choice == "4":
            manager.show_habits_rich()
            try:
                habit_id = int(input("Enter the ID of the habit: "))
                habit = manager.get_habit_by_id(habit_id)
                if habit:
                    streak = habit.get_streak()
                    console.print(f"[bold green]Current streak for '{habit.name}': {streak}[/bold green]")
                else:
                    console.print(f"[red]Habit with ID {habit_id} not found.[/red]")
            except ValueError:
                console.print("[red]Invalid input.[/red]")

        elif choice == "5":
            manager.show_habits_rich()
            try:
                habit_id = int(input("Enter the ID of the habit: "))
                habit = manager.get_habit_by_id(habit_id)
                if habit:
                    if habit.is_completed_today():
                        console.print(f"[green]Habit '{habit.name}' is already completed today.[/green]")
                    else:
                        console.print(f"[yellow]Habit '{habit.name}' is not yet completed today.[/yellow]")
                else:
                    console.print(f"[red]Habit with ID {habit_id} not found.[/red]")
            except ValueError:
                console.print("[red]Invalid input.[/red]")

        elif choice == "6":
            manager.show_habits_rich()
            try:
                habit_id = int(input("Enter the ID of the habit: "))
                habit = manager.get_habit_by_id(habit_id)
                if habit:
                    due = habit.next_due_date()
                    console.print(f"[bold cyan]Next due date for '{habit.name}': {due}[/bold cyan]")
                else:
                    console.print(f"[red]Habit with ID {habit_id} not found.[/red]")
            except ValueError:
                console.print("[red]Invalid input.[/red]")

        elif choice == "7":
            break
        else:
            console.print("[red]Invalid input.[/red]")

# --- Analysis menu ---

def show_analysis_menu(manager):
    """Submenu for analysis functions."""
    while True:
        console.print("\n[bold yellow]--- Analysis ---[/bold yellow]")
        print("1. Display habits by frequency")
        print("2. Display the longest series of a habit")
        print("3. Longest series of all habits")
        print("4. Back to main menu")

        choice = input("Please select an option (1–5): ")

        if choice == "1":
            # Display filtered habits by periodicity
            periodicity = input("What frequency (daily/weekly/monthly/yearly)? ")
            manager.load_habits()
            filtered = [h for h in manager.get_all_habits() if h.periodicity == periodicity]
            if not filtered:
                console.print("[red]No matching habits found.[/red]")
            else:
                manager.show_habits_rich_for(filtered, title=f"Habits ({periodicity})")

        elif choice == "2":
            # Longest series for a selected habit ID
            manager.load_habits()
            all_habits = manager.get_all_habits()
            manager.show_habits_rich_for(all_habits, title="All Habits")
            try:
                habit_id = int(input("Enter the ID of the habit: "))
                habit = manager.get_habit_by_id(habit_id)
                if habit:
                    streak = analysis.get_longest_streak_for_habit(habit_id)
                    if streak is None:
                        console.print(f"[red]Habit with ID {habit_id} not found in database.[/red]")
                    else:
                        console.print(f"[bold green]Longest streak for Habit {habit_id}: {streak}[/bold green]")
                else:
                    console.print(f"[red]Habit with ID {habit_id} not found.[/red]")
            except ValueError:
                console.print("[red]Invalid input.[/red]")

        elif choice == "3":
            # Longest streak across all habits
            manager.load_habits()
            streak = analysis.get_longest_streak_all_habits()
            console.print(f"[bold green]Longest streak of all habits: {streak} days[/bold green]")

        elif choice == "4":
            break
        else:
            console.print("[red]Invalid input.[/red]")

# --- Entry point ---

if __name__ == "__main__":
    main()
