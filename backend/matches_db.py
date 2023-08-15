import requests
import db_fns
import sqlite3 as sql
import time

def createMatchesDb():
    with sql.connect(db_fns.get_b2_db_filepath()) as conn:
        cursor = conn.cursor()
        cursor.execute((
            "CREATE TABLE IF NOT EXISTS "
            "matches("
                "id TEXT PRIMARY KEY,"
                "left_id TEXT, "
                "right_id TEXT, "
                "map TEXT, "
                "gametype TEXT, "
                "left_hero TEXT, "
                "left_tower_1 TEXT, "
                "left_tower_2 TEXT, "
                "left_tower_3 TEXT, "
                "right_hero TEXT, "
                "right_tower_1 TEXT, "
                "right_tower_2 TEXT, "
                "right_tower_3 TEXT, "
                "left_outcome TEXT, "
                "duration INTEGER, "
                "end_round INTEGER, "
                "time INTEGER"
            ")"
        ))
        conn.commit()

def fillMatchesDb():
    with sql.connect(db_fns.get_b2_db_filepath()) as conn:
        cursor = conn.cursor()
        user_ids = cursor.execute("SELECT user_id from players").fetchall()
        # select has funny output; change to 1d list in next line
        user_ids = [user_id for sublist in user_ids for user_id in sublist]
        for user_id in user_ids:
            # consider using sqlite native option?
            time_of_match = int(time.time())
            user_matches_url = f"https://data.ninjakiwi.com/battles2/users/{user_id}/matches"
            user_matches_json = requests.request("GET", user_matches_url).json()
            for user_match in user_matches_json["body"]:
                left_side = user_match["playerLeft"]
                right_side = user_match["playerRight"]
                match_id = user_match["id"]
                match_map = user_match["map"]
                match_gametype = user_match["gametype"]
                if (match_gametype != "Ranked"):
                    continue
                left_id = db_fns.profile_url_to_id(left_side["profileURL"])
                right_id = db_fns.profile_url_to_id(right_side["profileURL"])
                opp_side = user_match["playerLeft"] if not user_match['playerLeft']['currentUser'] else user_match["playerRight"]
                opp_id = db_fns.profile_url_to_id(opp_side["profileURL"])
                if opp_id not in user_ids:
                    # if opp not in hom, move to next person
                    break
                left_tower_1, left_tower_2, left_tower_3 = sorted([left_side["towerone"], left_side["towertwo"], left_side["towerthree"]])
                left_hero = left_side["hero"]
                right_tower_1, right_tower_2, right_tower_3 = sorted([right_side["towerone"], right_side["towertwo"], right_side["towerthree"]])
                right_hero = right_side["hero"]
                left_outcome = left_side["result"]
                match_duration = user_match["duration"]
                match_end_round = user_match["endRound"]
                insert_query = (
                    "INSERT OR IGNORE INTO Matches "
                    "(id, left_id, right_id, map, gametype, "
                    "left_hero, left_tower_1, left_tower_2, left_tower_3, "
                    "right_hero, right_tower_1, right_tower_2, right_tower_3, "
                    "left_outcome, duration, end_round, time) "
                    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
                )

                insert_vals = (
                    match_id, left_id, right_id, match_map, match_gametype, 
                    left_hero, left_tower_1, left_tower_2, left_tower_3, 
                    right_hero, right_tower_1, right_tower_2, right_tower_3, 
                    left_outcome, match_duration, match_end_round, time_of_match
                )

                cursor.execute(insert_query, insert_vals)
            time.sleep(0.6)
        conn.commit()
