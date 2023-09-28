import os
import psycopg
import dotenv
import requests
import re
import time

# get current season. Uses 1 api call
def current_season():
	homs_url = "https://data.ninjakiwi.com/battles2/homs"
	homs_data = requests.request("GET", homs_url).json()['body']

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

# get season index. Uses 1 api call
def season_from_num(season):
	homs_url = "https://data.ninjakiwi.com/battles2/homs"
	homs_data = requests.request("GET", homs_url).json()['body']
	pattern = re.compile(r'Season (\d+)')
	season_names = [pattern.search(hom_data['name']).group(1) for hom_data in homs_data]
	try:
		season_index = season_names.index(str(season))
		return homs_data[season_index]
	except ValueError:
		return None

def lb_total_pages(season):
	total_hom_players = season_from_num(current_season())["totalScores"]
	lb_page_count = (total_hom_players - 1) // 50 + 1
	return lb_page_count

# easier to store in db
def profile_url_to_id(url):
	user_id = url.split("/")[5]
	return user_id

# create get season from time function
dotenv.load_dotenv()

def db_conn():
	try:
		# Replace with your database connection details
		conn = psycopg.connect(
			dbname=os.getenv('DB_NAME'),
			user=os.getenv('DB_USER'),
			password=os.getenv('DB_PASSWORD'),
		)
		return conn
	except psycopg.Error as e:
		print("Error connecting to the database:", e)
		return None

def n_days_ago(n):
	now_time = int(time.time())
	past_time = now_time - 86400 * n
	return past_time