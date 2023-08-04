import requests
import db_fns
import sqlite3 as sql
import time

def createMatchesDb():
    conn = sql.connect(db_fns.get_b2_db_filepath())
    cursor = conn.cursor()
    cursor.execute((
        "CREATE TABLE IF NOT EXISTS "
        "matches("
            "id INTEGER PRIMARY KEY,"
            "user_id TEXT, "
            "opp_id TEXT, "
            "map TEXT, "
            "gametype TEXT, "
            "user_hero TEXT, "
            "user_tower_1 TEXT, "
            "user_tower_2 TEXT, "
            "user_tower_3 TEXT, "
            "opp_hero TEXT, "
            "opp_tower_1 TEXT, "
            "opp_tower_2 TEXT, "
            "opp_tower_3 TEXT, "
            "user_outcome TEXT, "
            "duration INTEGER, "
            "end_round INTEGER, "
            "time INTEGER, "
            "UNIQUE("
                "user_id, opp_id, map, gametype, "
                "user_hero, user_tower_1, user_tower_2, user_tower_3, "
                "opp_hero, opp_tower_1, opp_tower_2, opp_tower_3, "
                "user_outcome, duration, end_round"
            ")"
        ")"
    ))
    conn.commit()
    cursor.close()
    conn.close()

def fillMatchesDb():
    conn = sql.connect(db_fns.get_b2_db_filepath())
    cursor = conn.cursor()
    user_ids = cursor.execute("SELECT user_id from players").fetchall()
    for user_id in user_ids:
        user_id = user_id[0]
        # consider using sqlite native option?
        time_of_match = int(time.time())
        user_matches_url = f"https://data.ninjakiwi.com/battles2/users/{user_id}/matches"
        user_matches_json = requests.request("GET", user_matches_url).json()
        for user_match in user_matches_json["body"]:
            user_side = user_match["playerLeft"] if user_match['playerLeft']['currentUser'] else user_match["playerRight"]
            opp_side = user_match["playerLeft"] if not user_match['playerLeft']['currentUser'] else user_match["playerRight"]
            opp_id = db_fns.profile_url_to_id(opp_side["profileURL"])
            match_map = user_match["map"]
            match_gametype = user_match["gametype"]
            user_tower_1, user_tower_2, user_tower_3 = user_side["towerone"], user_side["towertwo"], user_side["towerthree"]
            user_hero = user_side["hero"]
            opp_tower_1, opp_tower_2, opp_tower_3 = opp_side["towerone"], opp_side["towertwo"], opp_side["towerthree"]
            opp_hero = opp_side["hero"]
            user_outcome = user_side["result"]
            match_duration = user_match["duration"]
            match_end_round = user_match["endRound"]
            insert_query = (
                "INSERT OR IGNORE INTO Matches "
                "(user_id, opp_id, map, gametype, "
                "user_hero, user_tower_1, user_tower_2, user_tower_3, "
                "opp_hero, opp_tower_1, opp_tower_2, opp_tower_3, "
                "user_outcome, duration, end_round, time) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            )

            insert_vals = (
                user_id, opp_id, match_map, match_gametype, 
                user_hero, user_tower_1, user_tower_2, user_tower_3, 
                opp_hero, opp_tower_1, opp_tower_2, opp_tower_3, 
                user_outcome, match_duration, match_end_round, time_of_match
            )

            cursor.execute(insert_query, insert_vals)
        print(user_id)
        time.sleep(0.6)
    conn.commit()
    cursor.close()
    conn.close()
