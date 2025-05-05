import requests
from bs4 import BeautifulSoup
from constants import BASE_URL, COLOUMN_NAMES, HEADERS, REQUST_TIMEOUT


class BrawlStatsScraper:
    def __init__(self):
        self.headers = HEADERS

    def get_player_url(self, player_id: str) -> str:
        """
        Create URL from player ID
        """
        try:
            return f"{BASE_URL}/{player_id}"
        except Exception as e:
            print(f"Error while creating URL: {e}")
            return ""

    def fetch_webpage(self, url: str):
        """
        Fetch the player's page from the internet
        """
        try:
            print(f"Fetching webpage from {url}...")
            response = requests.get(url, headers=self.headers, timeout=REQUST_TIMEOUT)
            response.raise_for_status()
            print("Request was successful.")
            return response.text
        except requests.exceptions.RequestException as error:
            print(f"Error fetching {url}: {error}")
            return None

    def extract_brawler_data(self, html_data: str):
        pass

    def get_player_brawlers(self, player_id: str):
        """
        Full pipeline: fetch webpage and extract brawler data
        """
        try:
            url = self.get_player_url(player_id)
            html_content = self.fetch_webpage(url)

            if not html_content:
                print(f"Failed to fetch data for player {player_id}")
                return []

            return self.extract_brawler_data(html_content)
        except Exception as e:
            print(f"Unexpected error in get_player_brawlers: {e}")
            return []


# if __name__ == "__main__":
#     player_id = "P9QRLG9RU"

#     scraper = BrawlStatsScraper()

#     #Create URL
#     print(">>> Testing URL creation")
#     url = scraper.get_player_url(player_id)
#     print("Generated URL:", url)

#     #Fetch webpage
#     print("\n>>> Testing page fetching")
#     html = scraper.fetch_webpage(url)
#     print("HTML length:", len(html) if html else "No content")

#     #Extract data
#     print("\n>>> Testing data extraction")
#     data = scraper.extract_brawler_data(html)

    # for index, brawler in enumerate(data, start=1):
    #     print(f"\n--- Brawler {index} ---")
    #     for column in COLOUMN_NAMES:
    #         value = brawler.get(column, "Not found")
    #         print(f"{column}: {value}")
