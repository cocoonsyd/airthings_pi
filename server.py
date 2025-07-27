import os
import sqlite3
from flask import Flask, jsonify, send_from_directory

DB_NAME = "airthings.db"
# Path to the built React app
STATIC_FOLDER = 'frontend/dist'

app = Flask(__name__, static_folder=STATIC_FOLDER)

def dict_factory(cursor, row):
    """Converts database rows into dictionaries."""
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

@app.route('/api/v1/readings', methods=['GET'])
def get_readings():
    """API endpoint to fetch all sensor readings from the database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    readings = cursor.execute("SELECT * FROM readings ORDER BY timestamp DESC").fetchall()
    conn.close()
    return jsonify(readings)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """
    Serves the React application.
    This handles routing by sending the index.html for any path not recognized by the API.
    """
    # If the requested path points to an existing file in the static folder, serve it.
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    # Otherwise, serve the main index.html (for the React router to handle).
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    # This part is for development only. In production, Gunicorn runs the 'app' object directly.
    app.run(host="0.0.0.0", port=5000, debug=True)
