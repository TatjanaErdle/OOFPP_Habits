# `README.md`

# Habit Tracker
This is a habit tracker written in Python as part of a portfolio project at IU International University. 
It showcases the practical application of both object-oriented programming (OOP) and functional programming (FP).

It is a simple Python application to create, track, and analyze personal habits using SQLite.

## Features
- Create new habits with name, description, and frequency
- Delete or complete habits
- Track streaks and due dates
- Analyze habits with summaries and statistics
- Console output with rich tables

## Tools & Frameworks
- Python 3.14
- PyCharm (development environment)
- Libraries: sqlite3, datetime, rich
- Database: SQLite

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/<dein-repo>/habit-tracker.git
   cd habit-tracker
2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate # Linux/Mac
    venv\Scripts\activate # Windows
3. Install dependencies (All required packages are listed in requirements.txt.):
    ```bash
   pip install -r requirements.txt
4. Initialize the database (The database will be created automatically on first startup, 
the CLI menu appears, and the tables are created.):
    ```bash
    python main.py

5. Run tests (The tests are run against a separate test database test_habits.db, 
so that the production data (habits.db) is not changed.):
    ```bash
    pytest -q

## Usage
Run the program and select from the menu:
1.Habit-specific actions
2.Show all habits
3.Analysis functions
4.Exit

## Database Structure
- **habits**: stores habit definitions (id, name, description, periodicity, created_at)
- **completions**: stores completion records (id, habit_id, completed_at)

## Testing
The project is tested using pytest. 
To run the automated tests, make sure you have pytest installed (it's included in requirements.txt). 
The tests run against a separate test database, test_habits.db, so the production data (habits.db) remains unchanged.

Start tests with:
```bash
    pytest -q
```

An overview of test coverage can be found in TESTS.md.

## Outlook
Future improvements may include reminders, visual dashboards, multi-user support, and exportable reports.

## Project structure
├── analysis.py
├── db.py
├── habit.py
├── habitmanager.py
├── main.py
├── test_project.py
├── test_fixture.sql
├── requirements.txt
├── README.md
└── TESTS.md





