import requests
import db_fns
import sqlite3 as sql
import time

def createMatchesDb():
    conn = sql.connect(db_fns.get_b2_db_filepath())
    cursor = conn.cursor()
    cursor.execute((
        "CREATE TABLE IF NOT EXISTS "
        "Matches(UserId, OppId, Map, Gametype, UserTrio, UserHero, OppTrio, OppHero, UserOutcome, Duration, EndRound)"
    ))
    conn.commit()
    cursor.close()
    conn.close()

def fillMatchesDb():
    conn = sql.connect(db_fns.get_b2_db_filepath())
    cursor = conn.cursor()
    user_ids = cursor.execute("SELECT UserId from Players").fetchall()
    for user_id in user_ids:
        user_id = user_id[0]
        user_matches_url = f"https://data.ninjakiwi.com/battles2/users/{user_id}/matches"
        user_matches_json = requests.request("GET", user_matches_url).json()
        for user_match in user_matches_json["body"]:
            user_side = user_match["playerLeft"] if user_match['playerLeft']['currentUser'] else user_match["playerRight"]
            opp_side = user_match["playerLeft"] if not user_match['playerLeft']['currentUser'] else user_match["playerRight"]
            opp_id = db_fns.profile_url_to_id(opp_side["profileURL"])
            match_map = user_match["map"]
            match_gametype = user_match["gametype"]
            user_trio = ','.join(sorted([user_side["towerone"], user_side["towertwo"], user_side["towerthree"]]))
            user_hero = user_side["hero"]
            opp_trio = ','.join(sorted([opp_side["towerone"], opp_side["towertwo"], opp_side["towerthree"]]))
            opp_hero = opp_side["hero"]
            user_outcome = user_side["result"]
            match_duration = user_match["duration"]
            match_end_round = user_match["endRound"]
            insert_query = (
                "INSERT INTO Matches "
                "(UserId, OppId, Map, Gametype, "
                "UserTrio, UserHero, OppTrio, OppHero, "
                "UserOutcome, Duration, EndRound) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
            )

            insert_vals = (
                user_id, opp_id, match_map, match_gametype,
                user_trio, user_hero, opp_trio, opp_hero,
                user_outcome, match_duration, match_end_round
            )

            cursor.execute(insert_query, insert_vals)
        print(user_id)
        time.sleep(0.6)
    conn.commit()
    cursor.close()
    conn.close()
