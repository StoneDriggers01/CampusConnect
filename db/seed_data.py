import sqlite3
import os

DB_PATH = "db/campusconnect.db"

# Remove existing DB for a clean seed (optional in dev environment)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Create tables manually or run schema.sql separately if preferred
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    preferences TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    location TEXT,
    date TEXT
)''')

c.execute('''CREATE TABLE IF NOT EXISTS external_events (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    date TEXT,
    location TEXT,
    description TEXT
)''')

# Create Users Seed Data
c.execute("INSERT INTO users (name, preferences) VALUES (?, ?)", ("Alice", "Aly"))
c.execute("INSERT INTO users (name, preferences) VALUES (?, ?)", ("Bob", "art, Bobby"))
c.execute("INSERT INTO users (name, preferences) VALUES (?, ?)", ("Charlie", "Chaz"))

# Internal Events Seed Data
c.execute("INSERT INTO events (title, location, date) VALUES (?, ?, ?)", ("Music Night", "Student Center", "2025-04-05"))
c.execute("INSERT INTO events (title, location, date) VALUES (?, ?, ?)", ("Hackathon", "Library", "2025-04-01"))
c.execute("INSERT INTO events (title, location, date) VALUES (?, ?, ?)", ("Art Exhibition", "Gallery", "2025-04-10"))

# External Events Seed Data (sample scraped-like data)
c.execute("INSERT INTO external_events (title, date, location, description) VALUES (?, ?, ?, ?)",
          ("Guest Lecture: AI in Education", "2025-04-15", "Main Auditorium", "A talk on the role of AI in modern education."))
c.execute("INSERT INTO external_events (title, date, location, description) VALUES (?, ?, ?, ?)",
          ("Spring Festival", "2025-04-20", "Campus Lawn", "Annual spring celebration with food, music, and games."))

conn.commit()
conn.close()