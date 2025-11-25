import os
from flask import Blueprint, render_template
import sqlite3

# Import your CampusEventScraper class
from utils.event_scraper import CampusEventScraper

event_bp = Blueprint('event', __name__)

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'db', 'campusconnect.db')
DB_PATH = os.path.abspath(DB_PATH)  # Ensures full absolute path

@event_bp.route("/events")
def events():
    # Step 1: Run the scraper to fetch and store external events
    scraper = CampusEventScraper("https://www.erskine.edu/events/", db_path=DB_PATH)
    scraper.run()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Step 2: Fetch internal events
    cursor.execute("SELECT title, location, date FROM events")
    internal_events = cursor.fetchall()
    print("Internal Events:", internal_events)  # Debugging

    # Step 3: Fetch external events from DB
    cursor.execute("SELECT title, date, location, description FROM external_events")
    external_events = cursor.fetchall()
    print("External Events:", external_events)  # Debugging

    conn.close()

    # Step 4: Pass both sets of events into template
    return render_template(
        "events.html",
        internal_events=internal_events,
        external_events=external_events
    )