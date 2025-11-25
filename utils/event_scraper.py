import requests
from bs4 import BeautifulSoup
import re
import sqlite3

DB_PATH = "db/campusconnect.db"

class CampusEventScraper:
    def __init__(self, url, db_path=DB_PATH):
        """
        Initialize with the campus events URL and database path.
        """
        self.url = url
        self.db_path = db_path

    def fetch_page(self):
        """
        Send GET request to the events page and return HTML content.
        Includes headers to mimic a real browser.
        """
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }

        try:
            response = requests.get(self.url, headers=headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.HTTPError as e:
            print(f"Failed to fetch events: {e}")
            return ""  # Return empty string so parse_events() won’t break

    def parse_events(self, html):
        """
        Parse HTML using BeautifulSoup to extract event details.
        Adjust selectors based on the structure of your college's event page.
        """
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        events = []

        # Example: Erskine College events page structure
        # Each event is inside a div with class 'tribe-events-calendar-list__event'
        event_divs = soup.find_all("div", class_="tribe-events-calendar-list__event")

        for div in event_divs:
            title = div.find("h3").get_text(strip=True) if div.find("h3") else "Untitled Event"
            date = div.find("time").get("datetime") if div.find("time") else None
            location = div.find("span", class_="tribe-events-venue-details").get_text(strip=True) if div.find("span", class_="tribe-events-venue-details") else "Unknown Location"
            description = div.find("div", class_="tribe-events-calendar-list__event-description").get_text(strip=True) if div.find("div", class_="tribe-events-calendar-list__event-description") else ""

            # Clean data with regex (remove extra whitespace, HTML entities, etc.)
            title = re.sub(r"\s+", " ", title)
            description = re.sub(r"\s+", " ", description)

            events.append({
                "title": title,
                "date": date,
                "location": location,
                "description": description
            })

        return events

    def save_events(self, events):
        """
        Store cleaned events into external_events table.
        """
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()

        for event in events:
            c.execute("""
                INSERT INTO external_events (title, date, location, description)
                VALUES (?, ?, ?, ?)
            """, (event["title"], event["date"], event["location"], event["description"]))

        conn.commit()
        conn.close()

    def run(self):
        """
        Main entry point: fetch page, parse events, save to DB.
        """
        html = self.fetch_page()
        events = self.parse_events(html)
        print(f"Extracted {len(events)} events.")
        if events:
            self.save_events(events)
            print("Events saved to external_events table.")
        else:
            print("No events scraped.")

if __name__ == "__main__":
    # Example usage with Erskine College events page
    scraper = CampusEventScraper("https://www.erskine.edu/events/")
    scraper.run()