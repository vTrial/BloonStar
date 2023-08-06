import db_fns
import matches_db
import players_db
import sqlite3 as sql
from flask import Flask, jsonify
from flask_cors import CORS
import schedule
import time
import threading
import json

app = Flask(__name__)
CORS(app)
db_lock = threading.Lock()

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

def update_databases():
    with db_lock:
        players_db.createPlayersDb()
        players_db.fillPlayersDb()
        print("created players")
        matches_db.createMatchesDb()
        matches_db.fillMatchesDb()
        print("created matches")

# Define the route to get user data
@app.route('/players', methods=['GET'])
def get_users():
    conn = sql.connect(db_fns.get_b2_db_filepath())
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM players")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({'users': users})

# Define the route to get match data
@app.route('/matches', methods=['GET'])
def get_matches():
    conn = sql.connect(db_fns.get_b2_db_filepath())
    cursor = conn.cursor()
    cursor.execute((
        "SELECT * FROM matches "
        "WHERE time > 1691125718 "
        "AND gametype = 'Ranked'"
    ))
    matches = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({'matches': matches})

@app.route('/matches/count', methods=['GET'])
def get_matches_count():
    conn = sql.connect(db_fns.get_b2_db_filepath())
    cursor = conn.cursor()
    cursor.execute((
        "SELECT COUNT(*) FROM matches "
        "WHERE time > 1691125718 "
        "AND gametype = 'Ranked'"
    ))
    matches = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return jsonify(matches)
@app.route('/towers/get', methods=['GET'])
def get_towers():
    conn = sql.connect(db_fns.get_b2_db_filepath())
    cursor = conn.cursor()
    tower_counts = {}
    for tower in towers:
        cursor.execute(
            f"SELECT "
            f"SUM(CASE WHEN user_tower_1 = '{tower}' THEN 1 ELSE 0 END) + "
            f"SUM(CASE WHEN user_tower_2 = '{tower}' THEN 1 ELSE 0 END) + "
            f"SUM(CASE WHEN user_tower_3 = '{tower}' THEN 1 ELSE 0 END) AS total_tower, "
            f"SUM(CASE WHEN user_tower_1 = '{tower}' AND user_outcome = 'win' THEN 1 ELSE 0 END) + "
            f"SUM(CASE WHEN user_tower_2 = '{tower}' AND user_outcome = 'win' THEN 1 ELSE 0 END) + "
            f"SUM(CASE WHEN user_tower_3 = '{tower}' AND user_outcome = 'win' THEN 1 ELSE 0 END) AS total_tower_wins "
            f"FROM Matches WHERE time > 1691125718 AND gametype = 'Ranked'"
        )
        row = cursor.fetchone()
        tower_count = row[0]
        tower_wins = row[1]
        tower_counts[tower] = {"games": tower_count, "wins": tower_wins}
    cursor.close()
    conn.close()
    return jsonify(tower_counts)
@app.route('/heroes/get', methods=['GET'])
def get_heroes():
    conn = sql.connect(db_fns.get_b2_db_filepath())
    cursor = conn.cursor()
    hero_counts = {}
    for hero in heroes:
        cursor.execute(
            f"SELECT "
            f"SUM(CASE WHEN user_hero = '{hero}' THEN 1 ELSE 0 END) AS total_hero, "
            f"SUM(CASE WHEN user_hero = '{hero}' AND user_outcome = 'win' THEN 1 ELSE 0 END) AS total_hero_wins "
            f"FROM Matches WHERE time > 1691125718 AND gametype = 'Ranked'"
        )
        row = cursor.fetchone()
        hero_count = row[0]
        hero_wins = row[1]
        hero_counts[hero] = {"games": hero_count, "wins": hero_wins}
    cursor.close()
    conn.close()
    return jsonify(hero_counts)
# Background task to update databases every minute
def update_databases_task():
    update_databases()
    while True:
        schedule.run_pending()
        time.sleep(1)

# Schedule the task to run every 60 minutes
schedule.every(60).minutes.do(update_databases)

if __name__ == '__main__':

    # Start the background task thread for periodic updates
    background_thread = threading.Thread(target=update_databases_task)
    background_thread.daemon = True
    background_thread.start()

    # Run the Flask app
    app.run(debug=True)
