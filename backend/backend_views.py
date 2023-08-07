import sqlite3 as sql
from flask import jsonify

import db_fns

towers = [
    "DartMonkey",
    "BoomerangMonkey",
    "BombShooter",
    "TackShooter",
    "IceMonkey",
    "GlueGunner",
    "SniperMonkey",
    "MonkeySub",
    "MonkeyBuccaneer",
    "MonkeyAce",
    "HeliPilot",
    "MortarMonkey",
    "DartlingGunner",
    "WizardMonkey",
    "SuperMonkey",
    "NinjaMonkey",
    "Alchemist",
    "Druid",
    "BananaFarm",
    "SpikeFactory",
    "MonkeyVillage",
    "EngineerMonkey",
]

heroes = [
    "Quincy",
    "Quincy_Cyber",
    "Gwendolin",
    "Gwendolin_Science",
    "StrikerJones",
    "StrikerJones_Biker",
    "Obyn",
    "Obyn_Ocean",
    "Churchill",
    "Churchill_Sentai",
    "Benjamin",
    "Benjamin_DJ",
    "Ezili",
    "Ezili_SmudgeCat",
    "PatFusty",
    "PatFusty_Snowman",
    "Agent_Jericho",
    "Highwayman_Jericho"
]

def get_users():
    # Route to get user data
    with sql.connect(db_fns.get_b2_db_filepath()) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM players")
        users = cursor.fetchall()

    return jsonify({'users': users})

def get_matches():
    # Route to get match data
    with sql.connect(db_fns.get_b2_db_filepath()) as conn:
        cursor = conn.cursor()
        cursor.execute((
            "SELECT * FROM matches "
            "WHERE time > 1691125718 "
            "AND gametype = 'Ranked'"
        ))
        matches = cursor.fetchall()

    return jsonify({'matches': matches})

def get_matches_count():
    # Route to get the count of matches
    with sql.connect(db_fns.get_b2_db_filepath()) as conn:
        cursor = conn.cursor()
        cursor.execute((
            "SELECT COUNT(*) FROM matches "
            "WHERE time > 1691125718 "
            "AND gametype = 'Ranked'"
        ))
        matches = cursor.fetchone()[0]

    return jsonify(matches)

def get_towers(match_map):
    # Route to get tower data
    with sql.connect(db_fns.get_b2_db_filepath()) as conn:
        cursor = conn.cursor()
        tower_counts = {}
        
        map_condition = f"AND map = '{match_map}'" if match_map else ""
        time_condition = "AND time > 1691125718"
        
        for tower in towers:
            cursor.execute(
                f"SELECT "
                f"SUM(CASE WHEN user_tower_1 = '{tower}' THEN 1 ELSE 0 END) + "
                f"SUM(CASE WHEN user_tower_2 = '{tower}' THEN 1 ELSE 0 END) + "
                f"SUM(CASE WHEN user_tower_3 = '{tower}' THEN 1 ELSE 0 END) AS total_tower, "
                f"SUM(CASE WHEN user_tower_1 = '{tower}' AND user_outcome = 'win' THEN 1 ELSE 0 END) + "
                f"SUM(CASE WHEN user_tower_2 = '{tower}' AND user_outcome = 'win' THEN 1 ELSE 0 END) + "
                f"SUM(CASE WHEN user_tower_3 = '{tower}' AND user_outcome = 'win' THEN 1 ELSE 0 END) AS total_tower_wins "
                f"FROM Matches WHERE gametype = 'Ranked' {time_condition} {map_condition}"
            )
            row = cursor.fetchone()
            tower_count = row[0]
            tower_wins = row[1]
            tower_counts[tower] = {"games": tower_count, "wins": tower_wins}

    return jsonify(tower_counts)

def get_heroes(match_map):
    # Route to get hero data
    with sql.connect(db_fns.get_b2_db_filepath()) as conn:
        cursor = conn.cursor()
        hero_counts = {}
        map_condition = f"AND map = '{match_map}'" if match_map else ""
        time_condition = "AND time > 1691125718"
        for hero in heroes:
            cursor.execute(
                f"SELECT "
                f"SUM(CASE WHEN user_hero = '{hero}' THEN 1 ELSE 0 END) AS total_hero, "
                f"SUM(CASE WHEN user_hero = '{hero}' AND user_outcome = 'win' THEN 1 ELSE 0 END) AS total_hero_wins "
                f"FROM Matches WHERE gametype = 'Ranked' {time_condition} {map_condition}"
            )
            row = cursor.fetchone()
            hero_count = row[0]
            hero_wins = row[1]
            hero_counts[hero] = {"games": hero_count, "wins": hero_wins}

    return jsonify(hero_counts)

