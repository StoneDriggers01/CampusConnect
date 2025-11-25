from flask import Blueprint, render_template
import sqlite3

from utils.api_client import APIClient

api_bp = Blueprint('api', __name__)

@api_bp.route("/api")
def api():
    # Step 1: Create an instance of APIClient and fetch alerts
    client = APIClient()
    client.run()  # fetches data from weather.gov and saves into api_data table

    # Step 2: Query the api_data table
    conn = sqlite3.connect("campusconnect.db")
    conn.row_factory = sqlite3.Row  # allows dict-like access
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, event, headline, description,
               severity, urgency, certainty,
               effective, expires, area, source
        FROM api_data
        ORDER BY effective DESC
    """)
    api_data = cursor.fetchall()
    conn.close()

    # Step 3: Pass results into template
    return render_template("api.html", api_data=api_data)