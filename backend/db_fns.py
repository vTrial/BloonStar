import os

# easier to store in db
def profile_url_to_id(url):
    user_id = url.split("/")[5]
    return user_id
def get_b2_db_filepath():
    return os.path.join(os.path.dirname(__file__), "b2db.db")