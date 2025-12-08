from flask import Blueprint, render_template
"""Imports Flask components for routing and rendering HTML templates."""

import sqlite3
"""Imports SQLite3 to enable database connections and queries."""

from utils.api_client import APIClient
"""Imports a custom APIClient class used to fetch weather alerts."""

api_bp = Blueprint('api', __name__)
"""Creates a Flask Blueprint named 'api' to modularize routes."""

@api_bp.route("/api")

def api():
    """Main function handling API data retrieval and rendering."""

    # Step 1: Create an instance of APIClient and fetch alerts
    client = APIClient()
    """Initializes the APIClient to interact with weather.gov."""

    client.run()  # fetches data from weather.gov and saves into api_data table
    """Runs the client to fetch alerts and store them in the database."""

    # Step 2: Query the api_data table
    conn = sqlite3.connect("campusconnect.db")
    """Opens a connection to the campusconnect.db SQLite database."""

    conn.row_factory = sqlite3.Row  # allows dict-like access
    """Configures rows to be accessed like dictionaries for readability."""

    cursor = conn.cursor()
    """Creates a cursor object to execute SQL queries."""

    cursor.execute("""
        SELECT id, event, headline, description,
               severity, urgency, certainty,
               effective, expires, area, source
        FROM api_data
        ORDER BY effective DESC
    """)
    """Executes SQL query to retrieve alert data ordered by effective date."""

    api_data = cursor.fetchall()
    """Fetches all rows returned by the query into a list."""

    conn.close()
    """Closes the database connection to free resources."""

    # Step 3: Pass results into template
    return render_template("api.html", api_data=api_data)
    """Renders the api.html template, passing in the retrieved alert data."""