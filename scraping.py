import requests

from bs4 import BeautifulSoup
from decompres_content import decode_bytes_to_string
from constants import BASE_URL, HEADERS, REQUST_TIMEOUT


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
        Fetch the player's page from the internet.
        Decompression and decoding are handled by utility functions.
        """
        try:
            print(f"Fetching webpage from {url}...")
            response = requests.get(url, headers=self.headers, timeout=REQUST_TIMEOUT)
            response.raise_for_status()
            print(f"Status Code: {response.status_code}")
            

            content_bytes = response.content
            
            final_html = decode_bytes_to_string(content_bytes, detected_encoding=response.encoding)

            if final_html:
                print(f"Successfully fetched and decoded HTML.")
            else:
                print("Failed to decode HTML content after fetching.")
            
            return final_html

        except requests.exceptions.RequestException as error:
            print(f"Error fetching {url}: {error}")
            return None
        except Exception as e:
            print(f"An unexpected error occurred in fetch_webpage: {e}")
            import traceback
            traceback.print_exc()
            return None

    def extract_brawler_data(self, html_data: str):
        if not html_data:
            return []

        soup = BeautifulSoup(html_data, "lxml")
        extracted_brawlers_list = []

        main_container_class = "_-8Sk_GrXg7so-YC4Vu-ff"
        main_container = soup.find("div", class_=main_container_class)

        if not main_container:
            print(f"Asosiy konteyner (class: '{main_container_class}') topilmadi.")
            return []
        
        brawler_card_a_tags = main_container.find_all('a', class_="_27S49vkmDiNCJywFvwR4qe")

        if not brawler_card_a_tags:
            return []

        for card_a_tag in brawler_card_a_tags:
            brawler_info = {}

            #get name
            name_div_container = card_a_tag.find("div", class_="_3-kW4dn2N1GeZqLIYP39Cb")
            if name_div_container:
                name_div = name_div_container.find("div", class_="_2PpbIDdt21EWrSBydkeVF4")
                brawler_info["Brawler"] = name_div.get_text(strip=True) if name_div else "N/A"
            else:
                brawler_info["Brawler"] = "N/A"

            #get rank
            rank_outer_div = card_a_tag.find("div", class_="_3FhYOci1Q4dYmBIzj25VGf")
            if rank_outer_div:
                rank_div = rank_outer_div.find("div", class_="_3lMfMVxY-knKo2dnVHMCWG _2__aet5G124QK1Wcdy2Aa-")
                try:
                    brawler_info["Rank"] = int(rank_div.get_text(strip=True)) if rank_div else 0
                except (ValueError, AttributeError):
                    brawler_info["Rank"] = 0
            else:
                brawler_info["Rank"] = 0
            
            #get level, current trophies and max trophies
            level_val, current_trophies_val, max_trophies_val = 0, 0, 0

            stats_container_main = card_a_tag.find("div", class_="_3fFggrqCh2FjEKkqTx0u1C")
            if stats_container_main:
                stat_blocks = stats_container_main.find_all("div", class_="_3JT8sOhwIbZHb6fsTTwi7E")
                for block in stat_blocks:
                    label_div = block.find("div", class_="_3lMfMVxY-knKo2dnVHMCWG _2jTl0GSnjD-2UDaZDIMqwr")
                    value_div_container = block.find("div", class_="_1rn865lAjZfN-4jC9VOvMG")

                    if label_div and value_div_container:

                        value_div = value_div_container.find("div", class_="_3lMfMVxY-knKo2dnVHMCWG") 
                        if value_div: 
                            label_text = label_div.get_text(strip=True).lower()
                            try:
                                numeric_value = int(value_div.get_text(strip=True))
                                if "level" in label_text: level_val = numeric_value
                                elif "current" in label_text: current_trophies_val = numeric_value
                                elif "highest" in label_text: max_trophies_val = numeric_value
                            except (ValueError, AttributeError):
                                pass 
            
            brawler_info["Level"] = level_val
            brawler_info["Current Trophies"] = current_trophies_val
            brawler_info["Max Trophies"] = max_trophies_val

            #get gadgets count and star powers
            gadgets_count, star_powers_count = 0, 0
            items_container = card_a_tag.find("div", class_="_3H-oc0Oc1Yme9D1WoHfk8a")
            if items_container:
                img_tags = items_container.find_all("img", class_="_2jWkKEvTH-ymjiategHCUE")
                for img in img_tags:
                    src_attr = img.get("src", "").lower()
                    if "gadgets/" in src_attr: gadgets_count += 1
                    elif "star-powers/" in src_attr: star_powers_count += 1
            
            brawler_info["Gadgets"] = gadgets_count
            brawler_info["Star Powers"] = star_powers_count
            
            extracted_brawlers_list.append(brawler_info)
            
        return extracted_brawlers_list





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
#     print(scraper.extract_brawler_data(html))

#     # for index, brawler in enumerate(data, start=1):
#     #     print(f"\n--- Brawler {index} ---")
#     #     for column in COLOUMN_NAMES:
#     #         value = brawler.get(column, "Not found")
#     #         print(f"{column}: {value}")
