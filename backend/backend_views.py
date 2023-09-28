from flask import jsonify

import bs_fns
import b2_consts

def time_query():
    return f"AND time > {bs_fns.n_days_ago(7)} "

def get_users():
    conn = bs_fns.db_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM players")
            users = cur.fetchall()

            return jsonify({'users': users})
    conn.close()

def get_matches():
    # Route to get match data
    conn = bs_fns.db_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute((
                "SELECT * FROM matches "
                "WHERE gametype = 'Ranked'"
            ))
            matches = cur.fetchall()

            return jsonify({'matches': matches})
    conn.close()


def get_matches_count():
    # Route to get the count of matches
    conn = bs_fns.db_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute((
                "SELECT COUNT(*) FROM matches "
                "WHERE gametype = 'Ranked'"
                f"{time_query()}"
            ))
            matches = cur.fetchone()[0]

            return jsonify(matches)
    conn.close()
    

def get_towers(match_map):
    # Route to get tower data
    conn = bs_fns.db_conn()
    with conn:
        with conn.cursor() as cur:
            tower_counts = {}
            
            map_condition = f"AND map = '{match_map}'" if match_map else ""

            for tower in b2_consts.towers:
                cur.execute(
                    f"SELECT "
                    f"SUM(CASE WHEN left_tower_1 = '{tower}' THEN 1 ELSE 0 END) + "
                    f"SUM(CASE WHEN left_tower_2 = '{tower}' THEN 1 ELSE 0 END) + "
                    f"SUM(CASE WHEN left_tower_3 = '{tower}' THEN 1 ELSE 0 END) + "
                    f"SUM(CASE WHEN right_tower_1 = '{tower}' THEN 1 ELSE 0 END) + "
                    f"SUM(CASE WHEN right_tower_2 = '{tower}' THEN 1 ELSE 0 END) + "
                    f"SUM(CASE WHEN right_tower_3 = '{tower}' THEN 1 ELSE 0 END) AS total_tower, "
                    f"SUM(CASE WHEN left_tower_1 = '{tower}' AND left_outcome = 'win' THEN 1 ELSE 0 END) + "
                    f"SUM(CASE WHEN left_tower_2 = '{tower}' AND left_outcome = 'win' THEN 1 ELSE 0 END) + "
                    f"SUM(CASE WHEN left_tower_3 = '{tower}' AND left_outcome = 'win' THEN 1 ELSE 0 END) + "
                    f"SUM(CASE WHEN right_tower_1 = '{tower}' AND left_outcome = 'lose' THEN 1 ELSE 0 END) + "
                    f"SUM(CASE WHEN right_tower_2 = '{tower}' AND left_outcome = 'lose' THEN 1 ELSE 0 END) + "
                    f"SUM(CASE WHEN right_tower_3 = '{tower}' AND left_outcome = 'lose' THEN 1 ELSE 0 END) AS total_tower_wins "
                    f"FROM Matches WHERE gametype = 'Ranked' {time_query()} {map_condition}"
                )
                row = cur.fetchone()
                tower_count = row[0]
                tower_wins = row[1]
                tower_counts[tower] = {"games": tower_count, "wins": tower_wins}

            return jsonify(tower_counts)
    conn.close()
    

def get_heroes(match_map):
    # Route to get hero data
    conn = bs_fns.db_conn()
    with conn:
        with conn.cursor() as cur:
            hero_counts = {}
            map_condition = f"AND map = '{match_map}'" if match_map else ""
            for hero in b2_consts.heroes:
                cur.execute(
                    f"SELECT "
                    f"SUM(CASE WHEN left_hero = '{hero}' THEN 1 ELSE 0 END) + "
                    f"SUM(CASE WHEN right_hero = '{hero}' THEN 1 ELSE 0 END) AS total_hero, "
                    f"SUM(CASE WHEN left_hero = '{hero}' AND left_outcome = 'win' THEN 1 ELSE 0 END) +"
                    f"SUM(CASE WHEN right_hero = '{hero}' AND left_outcome = 'lose' THEN 1 ELSE 0 END) AS total_hero_wins "
                    f"FROM Matches WHERE gametype = 'Ranked' {time_query()} {map_condition}"
                )
                row = cur.fetchone()
                hero_count = row[0]
                hero_wins = row[1]
                hero_counts[hero] = {"games": hero_count, "wins": hero_wins}

            return jsonify(hero_counts)
    conn.close()
    