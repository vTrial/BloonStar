import requests
import time

import bs_fns

def create():
    conn = bs_fns.db_conn()
    with conn:
        with conn.cursor() as cur:
            cursor = conn.cursor()
            cursor.execute((
                "CREATE TABLE IF NOT EXISTS "
                "matches("
                    "id TEXT primary key,"
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
                    "time INTEGER "
                ")"
            ))
    conn.close()
		


def fill():
    conn = bs_fns.db_conn()
    with conn:
        with conn.cursor() as cur:
            user_ids = cur.execute("select user_id from hom_users where season=14").fetchall()
            # select has funny output; change to 1d list in next line
            user_ids = [user_id for sublist in user_ids for user_id in sublist]
            user_count = len(user_ids)
            current_count = 0
            for user_id in user_ids:
                time_of_match = int(time.time())
                user_matches_url = f"https://data.ninjakiwi.com/battles2/users/{user_id}/matches"
                user_matches_json = requests.request("GET", user_matches_url).json()
                for user_match in user_matches_json["body"]:
                    left_side = user_match["playerLeft"]
                    right_side = user_match["playerRight"]
                    left_id = bs_fns.profile_url_to_id(left_side["profileURL"])
                    right_id = bs_fns.profile_url_to_id(right_side["profileURL"])
                    left_tower_1, left_tower_2, left_tower_3 = sorted([left_side["towerone"], left_side["towertwo"], left_side["towerthree"]])
                    right_tower_1, right_tower_2, right_tower_3 = sorted([right_side["towerone"], right_side["towertwo"], right_side["towerthree"]])
                    insert_query = (
                        "insert into matches "
                        "(id, left_id, right_id, map, gametype, "
                        "left_hero, left_tower_1, left_tower_2, left_tower_3, "
                        "right_hero, right_tower_1, right_tower_2, right_tower_3, "
                        "left_outcome, duration, end_round, time) "
                        "values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        "on conflict (id) do nothing"
                    )

                    insert_vals = (
                        user_match["id"], left_id, right_id, user_match["map"], user_match["gametype"], 
                        left_side["hero"], left_tower_1, left_tower_2, left_tower_3, 
                        right_side["hero"], right_tower_1, right_tower_2, right_tower_3, 
                        left_side["result"], user_match["duration"], user_match["endRound"], time_of_match
                    )

                    cur.execute(insert_query, insert_vals)
                current_count += 1
                print(f"{current_count}/{user_count} users processed")
                time.sleep(0.6)
            conn.commit()
    conn.close()
