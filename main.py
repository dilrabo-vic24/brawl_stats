"""
1. User Input:
    Prompt the user to input a player_id when the script is run.

2. URL Construction:
    Construct the URL using the player ID provided by the user:
        https://brawlstats.com/profile/{player_id}
        Example:
            https://brawlstats.com/profile/P9QRLG9RU

3. Web Scraping:
    Use BeautifulSoup to scrape the page and extract details about the brawler(s) associated with the given player.

4. Extract the Following Data:
    For each brawler, extract the following attributes:
        Brawler (e.g., SHELLY)
        Level
        Rank
        Current Trophies
        Max Trophies
        Gadgets
        Star Powers

    Example data: (SHELLY, 11, 25, 699, 759, 2, 1)

5. Store Data in Pandas DataFrame:
    Create a pandas DataFrame to store the extracted data with the following columns:
        ["Brawler", "Level", "Rank", "Current Trophies", "Max Trophies", "Gadgets", "Star Powers"]
    Clean the Data:
        Replace any NaN or Null values with 0.

6. Sorting:
    Sort the DataFrame by Max Trophies, Current Trophies, and Brawler in that order.

7. Create Another DataFrame for Brawlers with Level >= 9:
    Create a second DataFrame (df2) that contains only the brawlers with a Level >= 9.

8. Export to Excel:
    Use Openpyxl to save the data to an Excel file with two sheets:
        Sheet 1: Brawlers for regular games containing df.
        Sheet 2: Brawlers for ranked games containing df2.
    The file should be saved with a name based on the player_id and the current timestamp:
        {player_id}_{current_time}.xlsx
"""
import sys

from brawlers_data import brawlers_data
from scraping import BrawlStatsScraper
from brawler_data_pandas import BrawlerDataPandas
from excel_data_saver import ExcelDataSaver

def get_player_id() -> str:
    """
    Getting player_id from user and validate:
    """
    allowed_chars = set("PYLQGRJCUV0289")

    while True:
        player_id = input("Enter Brawl Stars player ID (e.g., P9QRLG9RU): ").strip().upper()

        if not player_id:
            print("Player ID cannot be empty. Please try again.")
            continue

        if not all(char in allowed_chars for char in player_id):
            print("Invalid characters in Player ID. Allowed letters: P, Y, L, Q, G, R, J, C, U, V and numbers: 0, 2, 8, 9.")
            continue

        return player_id
    
def main():
    try:
        print("Web scraping from brawlstats.com ")

        player_id = get_player_id()

        scraper = BrawlStatsScraper()
        # brawlers_data = scraper.get_player_brawlers(player_id=player_id)

        if not brawlers_data:
            print("\nError: Could not fetch brawler data. Please check the player ID and try again.")
            return
    

        print(f"Successfully fetched data for {len(brawlers_data)} brawlers")
        
        brawl_data_pandas = BrawlerDataPandas()
        df, df2 = brawl_data_pandas.create_dataframes(brawlers_data)


        print("Exporting to excel")
        excel_data_saver = ExcelDataSaver()

        file_path = excel_data_saver.export_to_excel(df, df2, player_id)

        print("\nExcel file created successfully:")
        print(f"  - {file_path}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", exc_info=True)
        print("\nAn unexpected error occurred. Please check the logs for details.")
        sys.exit(1)


        
if __name__ == "__main__":
    main()