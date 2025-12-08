import requests
"""Imports the requests library to handle HTTP requests to external APIs."""

import sqlite3
"""Imports SQLite3 to enable database connections and queries."""

import re
"""Imports the regex module for cleaning and formatting text."""

class APIClient:
    """Defines the APIClient class responsible for fetching and storing weather alerts."""

    BASE_URL = "https://api.weather.gov/alerts/active"
    """Sets the base URL for the weather.gov alerts API."""

    def __init__(self, db_path="campusconnect.db"):
        """Initializes the APIClient with a database path and ensures the table exists."""

        self.db_path = db_path
        """Stores the database path for later use in queries."""

        self.init_db()  # ensure table exists when client is created
        """Calls init_db to create the api_data table if it does not already exist."""

    def init_db(self):
        """Creates the api_data table if it doesn't exist."""

        conn = sqlite3.connect(self.db_path)
        """Opens a connection to the SQLite database using the provided path."""

        cursor = conn.cursor()
        """Creates a cursor object to execute SQL commands."""

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_data (
                id TEXT PRIMARY KEY,
                event TEXT,
                headline TEXT,
                description TEXT,
                severity TEXT,
                urgency TEXT,
                certainty TEXT,
                effective TEXT,
                expires TEXT,
                area TEXT,
                source TEXT
            )
        """)
        """Executes SQL command to create the api_data table with necessary fields."""

        conn.commit()
        """Commits the transaction to save changes to the database."""

        conn.close()
        """Closes the database connection to free resources."""

    def fetch_alerts(self, params=None):
        """
        Sends GET request to weather.gov alerts API.
        """

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            """Sends an HTTP GET request to the API with optional parameters and timeout."""

            response.raise_for_status()
            """Raises an exception if the response contains an HTTP error."""

            return response.json()
            """Returns the API response as a JSON object."""

        except requests.RequestException as e:
            """Handles any request-related exceptions."""

            print(f"Error fetching alerts: {e}")
            """Prints an error message if the request fails."""

            return None
            """Returns None when an error occurs."""

    def clean_text(self, text):
        """
        Cleans text using regex: remove HTML tags, normalize whitespace.
        """

        if not text:
            """Checks if the input text is empty or None."""

            return None
            """Returns None if no text is provided."""

        # Remove HTML tags
        text = re.sub(r"<.*?>", "", text)
        """Removes any HTML tags from the text using regex."""

        # Collapse multiple spaces/newlines
        text = re.sub(r"\s+", " ", text).strip()
        """Normalizes whitespace by collapsing multiple spaces/newlines into single spaces."""

        return text
        """Returns the cleaned text."""

    def save_alerts_to_db(self, data):
        """
        Parses JSON response and inserts into api_data table.
        """

        if not data or "features" not in data:
            """Checks if the data is valid and contains 'features'."""

            print("No valid data to insert.")
            """Prints a message if no valid data is available."""

            return
            """Exits the function early if data is invalid."""

        conn = sqlite3.connect(self.db_path)
        """Opens a connection to the SQLite database."""

        cursor = conn.cursor()
        """Creates a cursor object to execute SQL commands."""

        for feature in data["features"]:
            """Iterates through each feature in the API response."""

            props = feature.get("properties", {})
            """Extracts the 'properties' dictionary from each feature."""

            cursor.execute("""
                INSERT OR REPLACE INTO api_data (
                    id, event, headline, description,
                    severity, urgency, certainty,
                    effective, expires, area, source
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                feature.get("id"),
                self.clean_text(props.get("event")),
                self.clean_text(props.get("headline")),
                self.clean_text(props.get("description")),
                props.get("severity"),
                props.get("urgency"),
                props.get("certainty"),
                props.get("effective"),
                props.get("expires"),
                self.clean_text(props.get("areaDesc")),
                props.get("senderName")
            ))
            """Inserts or replaces alert data into the api_data table with cleaned values."""

        conn.commit()
        """Commits the transaction to save all inserted alerts."""

        conn.close()
        """Closes the database connection to free resources."""

        print("Alerts successfully saved to database.")
        """Prints confirmation that alerts were saved."""

    def run(self):
        """
        Full pipeline: fetch, clean, and store alerts.
        """

        data = self.fetch_alerts()
        """Fetches alerts from the API."""

        if data:
            """Checks if valid data was returned."""

            self.save_alerts_to_db(data)
            """Saves the fetched alerts into the database."""