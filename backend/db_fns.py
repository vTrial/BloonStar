import os
import psycopg
import dotenv
import requests

# easier to store in db
def profile_url_to_id(url):
    user_id = url.split("/")[5]
    return user_id

def get_lb_total_pages(season):
    homs_url = "https://data.ninjakiwi.com/battles2/homs"
    homs_data = requests.request("GET", homs_url).json()
    season_index = [hom_data['name'].split(" ")[1] for hom_data in homs_data["body"]].index(str(season))
    total_hom_players = homs_data['body'][season_index]["totalScores"]
    lb_page_count = (total_hom_players - 1) // 50 + 1
    return lb_page_count

# create get season from time function
dotenv.load_dotenv()

def get_database_connection():
    try:
        # Replace with your database connection details
        conn = psycopg.connect(
            dbname="bloonstar",
            user="postgres",
            password=os.getenv('PASSWORD'),
        )
        return conn
    except psycopg.Error as e:
        print("Error connecting to the database:", e)
        return None
