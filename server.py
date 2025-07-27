import sqlite3
from flask import Flask, jsonify

DB_NAME = "airthings.db"

app = Flask(__name__)

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
    
    # Fetch all readings, ordered by the most recent timestamp first
    readings = cursor.execute("SELECT * FROM readings ORDER BY timestamp DESC").fetchall()
    
    conn.close()
    
    return jsonify(readings)

if __name__ == '__main__':
    # Note: This is a development server. For deployment on the Pi,
    # we will use a more robust server like Gunicorn.
    # The 'host="0.0.0.0"' makes the server accessible from any device on your network.
    app.run(host="0.0.0.0", port=5000, debug=True)
