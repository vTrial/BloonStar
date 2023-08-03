import os
import sqlite3 as sqlite

# easier to store in db
def profile_url_to_id(url):
    user_id = url.split("/")[5]
    return user_id

# creates file in backend folder
b2_db_filepath = os.path.join(os.path.dirname(__file__), "b2db.db")
b2_db_connection = sqlite.connect(b2_db_filepath)
b2_db_cursor = b2_db_connection.cursor()