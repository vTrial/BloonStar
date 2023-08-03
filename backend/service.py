import db_fns
import matches_db
import players_db
import sqlite3 as sql
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def get_messages():
    conn = sql.connect(db_fns.get_b2_db_filepath())
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Players")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({'users': users})

if __name__ == '__main__':
    players_db.createPlayersDb()
    players_db.fillPlayersDb()
    app.run(debug=True)