#base url
BASE_URL = "https://brawlstats.com/profile"

#html elements
BRAWLER_CONTAINER = "brawler-container" 
BRAWLER_NAME = "brawler-name" 
BRAWLER_LEVEL = "brawler-level" 
BRAWLER_RANK = "brawler-rank"
BRAWLER_TROPHIES = "brawler-trophies"
BRAWLER_MAX_TROPHIES = "brawler-max-trophies"
BRAWLER_GADGETS = "brawler-gadgets"
BRAWLER_STAR_POWERS = "brawler-star-powers" 

#excel sheets
REGULAR_GAMES_SHEET = "Brawlers for regular games"
RANKED_GAMES_SHEET = "Brawlers for ranked games"

#Column names for DataFrame
COLOUMN_NAMES = [
    "Brawler",
    "Level",
    "Rank",
    "Current Trophies",
    "Max Trophies",
    "Gadgets",
    "Star Powers"
]

#header for http requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}
#time limit for http requests
REQUST_TIMEOUT = 10