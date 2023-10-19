import os
import dotenv
import requests
import re
import time
from supabase import create_client

# Load environment variables from a .env file if available
dotenv.load_dotenv(find_dotenv())

# Function to get the current season number from Ninja Kiwi's API
def current_season():
    # URL to retrieve the season data from Ninja Kiwi's API
    homs_url = "https://data.ninjakiwi.com/battles2/homs"
    # Send a GET request to the API and parse the JSON response
    homs_data = requests.request("GET", homs_url).json()['body']

    # Regular expression to match season numbers in the season name
    season_num_regex = r'Season (\d+)'

    # Find the first season that is marked as live (if available)
    for season_info in homs_data:
        if season_info['live']:
            return int(re.search(season_num_regex, season_info['name']).group(1))

    # If no live season is found, look for the first season with scores
    for season_info in homs_data:
        if season_info['totalScores'] > 0:
            return int(re.search(season_num_regex, season_info['name']).group(1))

    # If no live or scored season is found, return None or raise an exception
    return None  # You can choose to return None or raise an exception

# Function to get season info based on season number
def season_from_num(season):
    # URL to retrieve the season data from Ninja Kiwi's API
    homs_url = "https://data.ninjakiwi.com/battles2/homs"
    # Send a GET request to the API and parse the JSON response
    homs_data = requests.request("GET", homs_url).json()['body']
    pattern = re.compile(r'Season (\d+)')
    # Extract season numbers from season names
    season_names = [pattern.search(hom_data['name']).group(1) for hom_data in homs_data]
    try:
        # Find the index of the season matching the given season number
        season_index = season_names.index(str(season))
        return homs_data[season_index]
    except ValueError:
        return None

def lb_total_pages(season):
    total_hom_players = season_from_num(current_season())["totalScores"]
    # Calculate the number of pages based on the number of players (50 players per page)
    lb_page_count = (total_hom_players - 1) // 50 + 1
    return lb_page_count

def profile_url_to_id(url):
    user_id = url.split("/")[5]
    return user_id

# Prep supabase
def supabase_auth():
    url = os.getenv('VITE_SUPABASE_URL')
    key = os.getenv("VITE_SUPABASE_API_KEY")
    return create_client(url, key)
