import requests
import sqlite3
import re

class APIClient:
    BASE_URL = "https://api.weather.gov/alerts/active"

    def __init__(self, db_path="campusconnect.db"):
        self.db_path = db_path
        self.init_db()  # ensure table exists when client is created

    def init_db(self):
        """Create api_data table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
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
        conn.commit()
        conn.close()

    def fetch_alerts(self, params=None):
        """
        Sends GET request to weather.gov alerts API.
        """
        try:
            response = requests.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Error fetching alerts: {e}")
            return None

    def clean_text(self, text):
        """
        Cleans text using regex: remove HTML tags, normalize whitespace.
        """
        if not text:
            return None
        # Remove HTML tags
        text = re.sub(r"<.*?>", "", text)
        # Collapse multiple spaces/newlines
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def save_alerts_to_db(self, data):
        """
        Parses JSON response and inserts into api_data table.
        """
        if not data or "features" not in data:
            print("No valid data to insert.")
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        for feature in data["features"]:
            props = feature.get("properties", {})
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

        conn.commit()
        conn.close()
        print("Alerts successfully saved to database.")

    def run(self):
        """
        Full pipeline: fetch, clean, and store alerts.
        """
        data = self.fetch_alerts()
        if data:
            self.save_alerts_to_db(data)