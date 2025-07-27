import sqlite3

DB_NAME = "airthings.db"

def create_database():
    """Creates the SQLite database and the 'readings' table if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temperature REAL NOT NULL,
            humidity REAL NOT NULL,
            radon_short_term_avg REAL NOT NULL,
            radon_long_term_avg REAL NOT NULL,
            co2 REAL NOT NULL,
            voc REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
    print("Database and table are ready.")

if __name__ == '__main__':
    create_database()
