import sqlite3 as sql
from flask import Flask
from flask_cors import CORS
import schedule
import time
import threading

import db_fns
import matches_db
import players_db
import backend_views

app = Flask(__name__)
CORS(app)
db_lock = threading.Lock()

def update_databases():
    # Function to update the databases.
    with db_lock:
        # Create and/or fill players database table
        players_db.createPlayersDb()
        players_db.fillPlayersDb()
        print("created players")
        # Create and/or fill matches database table
        matches_db.createMatchesDb()
        matches_db.fillMatchesDb()
        print("created matches")

# Background task to update databases every minute
def update_databases_task():
    update_databases()
    while True:
        schedule.run_pending()
        time.sleep(1)

# Schedule the task to run every 60 minutes
schedule.every(60).minutes.do(update_databases)

# endpoints
app.add_url_rule('/users', view_func=backend_views.get_users)
app.add_url_rule('/matches', view_func=backend_views.get_matches)
app.add_url_rule('/matches/count', view_func=backend_views.get_matches_count)
app.add_url_rule('/towers/get', view_func=backend_views.get_towers)
app.add_url_rule('/heroes/get', view_func=backend_views.get_heroes)

if __name__ == '__main__':
    try:
        # Start the background task thread for periodic updates
        background_thread = threading.Thread(target=update_databases_task)
        background_thread.daemon = True
        background_thread.start()

        # Run the Flask app
        app.run(debug=True)
    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C) to exit the program gracefully.
        print("Keyboard interrupt received. Exiting...")
