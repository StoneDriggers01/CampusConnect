import sqlite3
"""Imports SQLite3 to enable database connections and queries."""

import os
"""Imports the os module to handle file operations like checking and removing files."""

DB_PATH = "db/campusconnect.db"
"""Defines the path to the SQLite database file campusconnect.db."""

# Remove existing DB for a clean seed (optional in dev environment)
if os.path.exists(DB_PATH):
    """Checks if the database file already exists."""

    os.remove(DB_PATH)
    """Removes the existing database file to start fresh (useful in development)."""

conn = sqlite3.connect(DB_PATH)
"""Opens a connection to the SQLite database at the specified path."""

c = conn.cursor()
"""Creates a cursor object to execute SQL commands."""

# Create tables manually or run schema.sql separately if preferred
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    preferences TEXT
)''')
"""Creates the users table with id, name, and preferences fields if it does not exist."""

c.execute('''CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    location TEXT,
    date TEXT
)''')
"""Creates the events table with id, title, location, and date fields if it does not exist."""

c.execute('''CREATE TABLE IF NOT EXISTS external_events (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    date TEXT,
    location TEXT,
    description TEXT
)''')
"""Creates the external_events table with id, title, date, location, and description fields."""

# Create Users Seed Data
c.execute("INSERT INTO users (name, preferences) VALUES (?, ?)", ("Alice", "Aly"))
"""Inserts a seed user Alice with preferences 'Aly' into the users table."""

c.execute("INSERT INTO users (name, preferences) VALUES (?, ?)", ("Bob", "art, Bobby"))
"""Inserts a seed user Bob with preferences 'art, Bobby' into the users table."""

c.execute("INSERT INTO users (name, preferences) VALUES (?, ?)", ("Charlie", "Chaz"))
"""Inserts a seed user Charlie with preferences 'Chaz' into the users table."""

# Internal Events Seed Data
c.execute("INSERT INTO events (title, location, date) VALUES (?, ?, ?)", ("Music Night", "Student Center", "2025-04-05"))
"""Inserts a seed internal event 'Music Night' into the events table."""

c.execute("INSERT INTO events (title, location, date) VALUES (?, ?, ?)", ("Hackathon", "Library", "2025-04-01"))
"""Inserts a seed internal event 'Hackathon' into the events table."""

c.execute("INSERT INTO events (title, location, date) VALUES (?, ?, ?)", ("Art Exhibition", "Gallery", "2025-04-10"))
"""Inserts a seed internal event 'Art Exhibition' into the events table."""

# External Events Seed Data (sample scraped-like data)
c.execute("INSERT INTO external_events (title, date, location, description) VALUES (?, ?, ?, ?)",
          ("Guest Lecture: AI in Education", "2025-04-15", "Main Auditorium", "A talk on the role of AI in modern education."))
"""Inserts a sample external event 'Guest Lecture: AI in Education' into the external_events table."""

c.execute("INSERT INTO external_events (title, date, location, description) VALUES (?, ?, ?, ?)",
          ("Spring Festival", "2025-04-20", "Campus Lawn", "Annual spring celebration with food, music, and games."))
"""Inserts a sample external event 'Spring Festival' into the external_events table."""

conn.commit()
"""Commits all changes to the database to ensure data is saved."""

conn.close()
"""Closes the database connection to free resources."""