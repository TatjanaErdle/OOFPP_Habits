# `README.md`

# Habit Tracker

The **Habit Tracker** is a Python application developed as part of a portfolio project at IU International University.

It demonstrates the practical application of **object-oriented programming (OOP)**, **functional programming (FP)**, and **test-driven development (TDD)** using **pytest**.

The application allows users to create, track, analyze, and visualize personal habits using an SQLite database.  

It includes a fully automated test suite with both **unit tests** and **integration tests**, ensuring correctness,  
reproducibility, and maintainability.

---

## Table of Contents 
1. [Overview](#overview) 
2. [Features](#features) 
3. [Tools & Frameworks](#tools--frameworks) 
4. [Installation](#installation) 
5. [Architecture](#architecture) 
6. [Why This Architecture?](#why-this-architecture) 
7. [Learning Outcomes](#learning-outcomes) 
8. [Usage](#usage) 
9. [Database Initialization & Demo Data](#database-initialization--demo-data) 
10. [Database Structure](#database-structure) 
11. [Testing Strategy](#testing-strategy) 
12. [Project Structure](#project-structure) 
13. [Outlook](#outlook)


--- 

## Overview 
The Habit Tracker is a console-based application that helps users build and maintain positive habits. 

It combines: 

- **OOP** for modeling habits and managing application logic 
- **FP** for analytics and pure data transformations 
- **SQLite** for persistent storage
- **pytest** for automated testing (unit, integration, and functional requirements tests) 

The project is intentionally lightweight and portable (no external services or servers required). 

---

## Features

The Habit Tracker provides a complete workflow for managing personal habits:

### ✔ Habit Management
- Create new habits with name, description, and periodicity (daily, weekly, monthly, yearly)
- Edit existing habits
- Delete habits (including all associated completion records)
- Mark habits as completed

### ✔ Tracking & Analytics
- Automatic streak calculation (daily, weekly, monthly, yearly)
- Determine whether a habit is **due**, **done**, or **overdue**
- Compute longest streaks per habit or across all habits
- Analyze habits by periodicity
- Display all habits with statistics

### ✔ User Interface
- Console-based interface
- Rich table output using the `rich` library
- Clear menu navigation

### ✔ Persistence
- All data is stored in a local SQLite database (`habits.db`)
- Data is **not overwritten** on restart
- Demo data is imported only once on first startup

---

## Tools & Frameworks

| Component | Description |
|----------|-------------|
| **Python 3.14** | Programming language |
| **SQLite** | Lightweight relational database |
| **pytest** | Automated testing framework |
| **rich** | Console formatting and tables |
| **freezegun** | Freezes time for deterministic tests |
| **PyCharm** | Development environment |

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/TatjanaErdle/OOFPP_Habits.git
   cd OOFPP_Habits
   ```
2. Create and activate a virtual environment:
    ```bash
    # Linux/Mac:
    source venv/bin/activate
    # Windows (PowerShell oder CMD):
    venv\Scripts\activate
   ```
3. Install dependencies (All required packages are listed in requirements.txt.):
    ```bash
   pip install -r requirements.txt
   ```
4. Initialize the database:
    ```bash
    python main.py
   ```

5. Run tests (The tests are run against a separate test database test_habits.db, 
so that the production data (habits.db) is not changed.):
    ```bash
    pytest -q
   ```
   
On first startup:
- The database is created automatically 
- Demo data from test_fixture.sql is imported (only if the DB is empty)
- The CLI menu appears

### Troubleshooting

If the application does not start, check the following:

- Python 3.10+ is installed and available in your PATH  
- The virtual environment is activated  
- Dependencies were installed via `pip install -r requirements.txt`  
- You are running `python main.py` from the project root directory  

These are general Python setup issues and not specific to the Habit Tracker.

---

## Architecture
The application follows a modular, layered architecture:

### 1. Habit (habit.py)
Represents a single habit with:
- id
- name
- description
- periodicity
- created_at

Includes logic for:
- streak calculation
- due/overdue checks
- completion tracking
- next due date

### 2. HabitManager (habitmanager.py)
Acts as the interface between:
- the CLI 
- the database 
- the Habit objects

Responsibilities:
- CRUD operations 
- loading habits 
- marking completions 
- generating statistics 
- rendering rich tables

### 3. Database Layer (db.py)
Contains all SQL operations:
- create tables 
- add habits 
- delete habits 
- fetch completions 
- mark completions 
- import demo data

### 4. Analytics (analysis.py)
Provides pure FP-style functions:
- longest streak per habit 
- longest streak overall 
- list habits by periodicity 
- list all habits

### 5. Tests (test_project.py)
Covers:
- Habit logic (unit tests)
- HabitManager logic (integration tests)
- Database operations 
- Analytics functions 
- Streak calculations with frozen time

---

## Why this Architecture?
The architecture was chosen deliberately to demonstrate clean separation of concerns:

### OOP for domain modeling
Habits are real-world entities with behavior (streaks, due dates, completions).
Encapsulating this logic in a class makes the system intuitive and maintainable.

### FP for analytics
Analytics functions are:
- pure 
- stateless 
- deterministic 
- easy to test

This cleanly separates business logic from data transformation.

### Dedicated database layer
All SQL operations are centralized in db.py, ensuring:
- no SQL duplication
- no SQL in UI or business logic
- easy maintainability
- clean testability

### Manager layer for orchestration
HabitManager coordinates:
- Habit objects
- database operations
- CLI interactions

This avoids “fat models” and keeps responsibilities clear.

### Full test suite
The architecture supports:
- isolated unit tests
- realistic integration tests
- functional requirements validation

This ensures correctness and long-term maintainability.

---

## Learning Outcomes

This project demonstrates mastery of:

### Object-Oriented Programming
- Class design 
- Encapsulation 
- Method behavior 
- Separation of concerns

### Functional Programming
- Pure functions 
- Deterministic analytics 
- No side effects 
- Testability through immutability

### Test-Driven Development
- Unit tests 
- Integration tests 
- Functional requirements tests 
- Use of monkeypatch and fake objects 
- Deterministic time with freezegun

### Database Design
- SQL schema design 
- Foreign keys 
- Persistent storage 
- Fixture-based initialization

### Software Architecture
- Layered design 
- Clean interfaces 
- Maintainability 
- Extensibility

### CLI Application Development
- User interaction 
- Menu navigation 
- Rich console output

---

## Usage
After starting the program, the main menu appears:
1. Habit-specific actions
2. Analysis 
3. Exit

<img width="311" height="126" alt="image" src="https://github.com/user-attachments/assets/926a1384-b142-40f2-be74-68b40833e532" />

### Example: Creating a new habit
The user is prompted for:
- name 
- description 
- periodicity

The habit is saved in the database and immediately visible.

<img width="547" height="322" alt="image" src="https://github.com/user-attachments/assets/b18702f4-536e-4278-a009-ec59b5061a59" />

### Example: Completing a habit
The user selects a habit ID → completion is stored with timestamp.

<img width="1345" height="532" alt="image" src="https://github.com/user-attachments/assets/638cf4a7-d955-424a-a164-f91dee2562eb" />

### Example: Viewing all habits
Displays a rich table with:
- ID
- Name 
- Description 
- Periodicity 
- Streak
- Status (DONE / DUE / OVERDUE)
- Created at 
- Last completion

<img width="1350" height="542" alt="image" src="https://github.com/user-attachments/assets/5ef8902e-dc6a-4ee1-8dd6-60548a60ea58" />

---

## Database Initialization & Demo Data

### Automatic Initialization

### On first startup:
1. habits.db is created
2. Tables habits and completions are created
3. If the database is empty, test_fixture.sql is imported

This ensures:
- The user sees meaningful demo data immediately 
- The app is fully functional without manual setup 
- The same data used in integration tests is available in the app 

### Demo Data (test_fixture.sql)
The fixture contains:
- 5 predefined habits
- 4 weeks of completion data for daily and weekly habits
- 1 monthly completion for the monthly habit

The dataset is used:
- in the application
- in integration tests
- for streak validation

The demo data is only imported once.
User-created habits remain permanently stored.

### Resetting the database

If the database already contains data, the fixture will not be reloaded.
To reload the test data:
- Exit the application 
- Delete habits.db
- Restart the application 

The database will be recreated and populated automatically.

### Database Structure

#### Table habits
- id (INTEGER): Primary key
- name (TEXT): Habit name
- description (TEXT): Habit description
- periodicity (TEXT): daily/weekly/monthly/yearly
- created_at (TEXT): Timestamp

#### Table completions
- id (INTEGER): Primary key
- habit_id (INTEGER): Foreign key to habits.id
- completed_at (TEXT): Timestamp

---

## Testing strategy
The project uses a clearly structured testing pyramid to validate both isolated logic and module interaction.

Tests are divided into:
- Unit tests
- Functional requirements tests 
- Integration tests

All tests run against a separate test database (test_habits.db) to avoid modifying production data.

#### Deterministic Time
freezegun freezes the date (e.g., 2025‑11‑16) to ensure reproducible streak calculations.

Start tests with:
```bash
pytest -q
```
An overview of test coverage can be found in TESTS.md.

### Unit tests
Unit tests check pure logic only, without external dependencies such as databases or files.
They cover:
- Habit logic (create, edit, delete)
- Analytics module (functional programming)
- Use of monkeypatch to isolate DB accesses 
- Fake objects (FakeConn, FakeCursor) to simulate the database

These tests are fast, deterministic, and independent of the environment.

### Functional requirements tests
A separate test class explicitly checks the functional requirements defined in the task:
- Habits can be created.
- Habits can be edited. 
- Habits can be deleted. 
- Completions can be recorded. 
- All four analytics functions work. 
- The 4-week test data provides correct streaks.

These tests show that the system fully meets the required functions.

### Integration tests
Integration tests check the interaction of several modules with a real SQLite test database, which is reproducibly built from a 4-week SQL fixture before each test run.

They test:
- db.py (CRUD operations, completions)
- Habit with real data 
- HabitManager (loading, creating, deleting, completing)
- Analytics functions with real time series 
- Streak calculations using freezegun

These tests validate the real behavior of the system.

### Test pyramid
                ▲
                │  (optional)
                │  End-to-End Tests
        ┌───────────────────────────┐
        │     Integration Tests     │
        │  - DB + SQL-Fixture       │
        │  - HabitManager           │
        │  - Analytics (real data)  │
        └───────────────────────────┘
                ▲
                │  
                │  
        ┌───────────────────────────┐
        │        Unit Tests         │
        │  - Habit CRUD             │
        │  - Analytics (FP)         │
        │  - monkeypatch + Fakes    │
        └───────────────────────────┘

---

## Project Structure

The following files make up the Habit Tracker project. Each file has a clearly defined role:


├── analysis.py          # Analytics functions

├── db.py                # Database layer

├── habit.py             # Habit class

├── habitmanager.py      # Manager class (CRUD, UI, logic)

├── main.py              # CLI entry point

├── test_project.py      # Full test suite

├── test_fixture.sql     # Demo + test data (4-week dataset)

├── requirements.txt     # Dependencies

├── README.md            # Documentation

└── TESTS.md             # Additional test documentation

---

## Outlook 

Possible future improvements:
- Reminder notifications
- Graphical dashboard (matplotlib or web UI)
- Multi-user support
- Export/import of habits (JSON/CSV)
- Cloud synchronization
- Mobile app version










