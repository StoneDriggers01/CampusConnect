-- SQLite schema
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    preferences TEXT
);

DROP TABLE IF EXISTS events;
CREATE TABLE events (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    location TEXT,
    date TEXT
);

-- External scraped events table
DROP TABLE IF EXISTS external_events;
CREATE TABLE external_events (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    date TEXT,
    location TEXT,
    description TEXT
);