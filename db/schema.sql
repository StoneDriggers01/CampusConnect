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

-- API data table for weather.gov alerts
DROP TABLE IF EXISTS api_data;
CREATE TABLE api_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event TEXT NOT NULL,                 
    headline TEXT,                       
    description TEXT,                    
    severity TEXT,                       
    urgency TEXT,                       
    certainty TEXT,                 
    effective TEXT,                   
    expires TEXT,                    
    area TEXT,                         
    source TEXT
    alert TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP                
);

    