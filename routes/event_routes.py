import os
"""Imports the os module to handle file paths and directory operations."""

from flask import Blueprint, render_template
"""Imports Flask components for modular routing and rendering HTML templates."""

import sqlite3
"""Imports SQLite3 to enable database connections and queries."""

# Import your CampusEventScraper class
from utils.event_scraper import CampusEventScraper
"""Imports the custom CampusEventScraper class used to fetch external events."""

event_bp = Blueprint('event', __name__)
"""Creates a Flask Blueprint named 'event' to group event-related routes."""

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'campusconnect.db')
"""Constructs the relative path to the campusconnect.db database file."""

DB_PATH = os.path.abspath(DB_PATH)  # Ensures full absolute path
"""Converts the relative path into an absolute path for reliability."""

@event_bp.route("/events")

def events():
    """Main function handling event scraping, database queries, and template rendering."""

    # Step 1: Run the scraper to fetch and store external events
    scraper = CampusEventScraper("https://www.erskine.edu/events/", db_path=DB_PATH)
    """Initializes the scraper with the Erskine events URL and database path."""

    scraper.run()
    """Runs the scraper to fetch external events and store them in the database."""

    conn = sqlite3.connect(DB_PATH)
    """Opens a connection to the SQLite database using the absolute path."""

    cursor = conn.cursor()
    """Creates a cursor object to execute SQL queries."""

    # Step 2: Fetch internal events
    cursor.execute("SELECT title, location, date FROM events")
    """Executes SQL query to retrieve internal events from the events table."""

    internal_events = cursor.fetchall()
    """Fetches all internal event rows returned by the query."""

    print("Internal Events:", internal_events)  # Debugging
    """Prints internal events to console for debugging purposes."""

    # Step 3: Fetch external events from DB
    cursor.execute("SELECT title, date, location, description FROM external_events")
    """Executes SQL query to retrieve external events from the external_events table."""

    external_events = cursor.fetchall()
    """Fetches all external event rows returned by the query."""

    print("External Events:", external_events)  # Debugging
    """Prints external events to console for debugging purposes."""

    conn.close()
    """Closes the database connection to free resources."""

    # Step 4: Pass both sets of events into template
    return render_template(
        "events.html",
        internal_events=internal_events,
        external_events=external_events
    )
    """Renders the events.html template, passing both internal and external events."""