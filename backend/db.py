import sqlite3 as sqlite
import os
import requests

# for paginating lb
def get_lb_total_pages():
    homs_url = "https://data.ninjakiwi.com/battles2/homs"
    homs_data = requests.request("GET", homs_url).json()
    total_hom_players = homs_data['body'][0]["totalScores"]
    lb_page_count = (total_hom_players - 1) // 50 + 1
    return lb_page_count

# easier to store in db
def profile_url_to_id(url):
    user_id = url.split("/")[5]
    return user_id

# create players db if doesn't exist
def createPlayersDatabase(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS Players(DisplayName, Score, UserId PRIMARY KEY)")

def fillPlayersDatabase(cursor, connection):
    lb_total_pages = get_lb_total_pages()
    for lb_page_num in range(1, lb_total_pages + 1):
        lb_url = f"https://data.ninjakiwi.com/battles2/homs/season_12/leaderboard?page={lb_page_num}"
        lb_json = requests.request("GET", lb_url).json()
        if lb_json["success"]:
            for player in lb_json["body"]:
                user_id = profile_url_to_id(player["profile"])
                insert_replace_query = (
                    "INSERT OR REPLACE INTO Players (DisplayName, Score, UserId) "
                    "VALUES (?, ?, ?)"
                )
                insert_replace_vals = (player['displayName'], player['score'], user_id)
                cursor.execute(insert_replace_query, insert_replace_vals)
    connection.commit()

# creates file in backend folder
b2_db_filepath = os.path.join(os.path.dirname(__file__), "b2db.db")
b2_db_connection = sqlite.connect(b2_db_filepath)
b2_db_cursor = b2_db_connection.cursor()

createPlayersDatabase(b2_db_cursor)
fillPlayersDatabase(b2_db_cursor, b2_db_connection)
res = b2_db_cursor.execute("SELECT DisplayName from Players")
print(len(res.fetchall()))