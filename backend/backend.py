from flask import Flask
from flask_cors import CORS

import backend_views

app = Flask(__name__)
CORS(app)

# endpoints
# app.add_url_rule('/users', view_func=backend_views.get_users)
app.add_url_rule('/matches', view_func=backend_views.get_matches)
app.add_url_rule('/matches/count', view_func=backend_views.get_matches_count)
app.add_url_rule('/towers/get/', defaults={'match_map': ""}, view_func=backend_views.get_towers)
app.add_url_rule('/towers/get/<match_map>', view_func=backend_views.get_towers)
app.add_url_rule('/heroes/get/', defaults={'match_map': ""}, view_func=backend_views.get_heroes)
app.add_url_rule('/heroes/get/<match_map>', view_func=backend_views.get_heroes)

if __name__ == '__main__':
    try:

        # Run the Flask app
        app.run(debug=True)
    except KeyboardInterrupt:
        # Handle keyboard interrupt (Ctrl+C) to exit the program gracefully.
        print("Keyboard interrupt received. Exiting...")
