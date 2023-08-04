import db_fns
import matches_db
import players_db
import sqlite3 as sql
from flask import Flask, jsonify
import schedule
import time
import threading

app = Flask(__name__)
db_lock = threading.Lock()

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
    cursor.execute("SELECT * FROM Players")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({'users': users})

# Define the route to get match data
@app.route('/matches', methods=['GET'])
def get_matches():
    conn = sql.connect(db_fns.get_b2_db_filepath())
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Matches")
    matches = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({'matches': matches})

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
