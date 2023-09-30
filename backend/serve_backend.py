from waitress import serve
from backend import app

if __name__ == '__main__':
    # Use Waitress to serve your app
    serve(app, host='0.0.0.0', port=5000)