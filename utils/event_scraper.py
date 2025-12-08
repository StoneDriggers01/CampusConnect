import requests
"""Imports the requests library to send HTTP requests to external websites."""

from bs4 import BeautifulSoup
"""Imports BeautifulSoup for parsing and extracting data from HTML content."""

import re
"""Imports the regex module for cleaning and normalizing text."""

import sqlite3
"""Imports SQLite3 to enable database connections and queries."""

DB_PATH = "db/campusconnect.db"
"""Defines the default path to the campusconnect.db SQLite database."""

class CampusEventScraper:
    """Defines the CampusEventScraper class for fetching, parsing, and storing event data."""

    def __init__(self, url, db_path=DB_PATH):
        """
        Initialize with the campus events URL and database path.
        """

        self.url = url
        """Stores the URL of the events page to be scraped."""

        self.db_path = db_path
        """Stores the database path for saving scraped events."""

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
        """Defines HTTP headers to mimic a browser and avoid request blocking."""

        try:
            response = requests.get(self.url, headers=headers)
            """Sends an HTTP GET request to the events page using the defined headers."""

            response.raise_for_status()
            """Raises an exception if the response contains an HTTP error."""

            return response.text
            """Returns the HTML content of the page as text."""

        except requests.exceptions.HTTPError as e:
            """Handles HTTP errors during the request."""

            print(f"Failed to fetch events: {e}")
            """Prints an error message if the request fails."""

            return ""  # Return empty string so parse_events() won’t break
            """Returns an empty string to prevent parse_events() from breaking."""

    def parse_events(self, html):
        """
        Parse HTML using BeautifulSoup to extract event details.
        Adjust selectors based on the structure of your college's event page.
        """

        if not html:
            """Checks if HTML content is empty."""

            return []
            """Returns an empty list if no HTML is provided."""

        soup = BeautifulSoup(html, "html.parser")
        """Parses the HTML content using BeautifulSoup."""

        events = []
        """Initializes an empty list to store extracted events."""

        # Example: Erskine College events page structure
        # Each event is inside a div with class 'tribe-events-calendar-list__event'
        event_divs = soup.find_all("div", class_="tribe-events-calendar-list__event")
        """Finds all event containers in the HTML based on their CSS class."""

        for div in event_divs:
            """Iterates through each event container."""

            title = div.find("h3").get_text(strip=True) if div.find("h3") else "Untitled Event"
            """Extracts the event title or assigns 'Untitled Event' if missing."""

            date = div.find("time").get("datetime") if div.find("time") else None
            """Extracts the event date from the <time> tag or sets None if missing."""

            location = div.find("span", class_="tribe-events-venue-details").get_text(strip=True) if div.find("span", class_="tribe-events-venue-details") else "Unknown Location"
            """Extracts the event location or assigns 'Unknown Location' if missing."""

            description = div.find("div", class_="tribe-events-calendar-list__event-description").get_text(strip=True) if div.find("div", class_="tribe-events-calendar-list__event-description") else ""
            """Extracts the event description or assigns an empty string if missing."""

            # Clean data with regex (remove extra whitespace, HTML entities, etc.)
            title = re.sub(r"\s+", " ", title)
            """Cleans the title by collapsing multiple spaces into one."""

            description = re.sub(r"\s+", " ", description)
            """Cleans the description by collapsing multiple spaces into one."""

            events.append({
                "title": title,
                "date": date,
                "location": location,
                "description": description
            })
            """Appends the cleaned event details as a dictionary to the events list."""

        return events
        """Returns the list of parsed and cleaned events."""

    def save_events(self, events):
        """
        Store cleaned events into external_events table.
        """

        conn = sqlite3.connect(self.db_path)
        """Opens a connection to the SQLite database."""

        c = conn.cursor()
        """Creates a cursor object to execute SQL commands."""

        for event in events:
            """Iterates through each event in the events list."""

            c.execute("""
                INSERT INTO external_events (title, date, location, description)
                VALUES (?, ?, ?, ?)
            """, (event["title"], event["date"], event["location"], event["description"]))
            """Inserts event details into the external_events table."""

        conn.commit()
        """Commits the transaction to save all inserted events."""

        conn.close()
        """Closes the database connection to free resources."""

    def run(self):
        """
        Main entry point: fetch page, parse events, save to DB.
        """

        html = self.fetch_page()
        """Fetches the HTML content of the events page."""

        events = self.parse_events(html)
        """Parses the HTML content to extract event details."""

        print(f"Extracted {len(events)} events.")
        """Prints the number of events extracted for debugging."""

        if events:
            """Checks if any events were successfully scraped."""

            self.save_events(events)
            """Saves the scraped events into the database."""

            print("Events saved to external_events table.")
            """Prints confirmation that events were saved."""

        else:
            """Handles the case where no events were scraped."""

            print("No events scraped.")
            """Prints a message indicating no events were found."""

if __name__ == "__main__":
    # Example usage with Erskine College events page
    scraper = CampusEventScraper("https://www.erskine.edu/events/")
    """Creates a scraper instance with the Erskine College events page URL."""

    scraper.run()
    """Runs the scraper to fetch, parse, and save events."""