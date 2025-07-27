import sqlite3
import random
from datetime import datetime

# --- HOW TO ADAPT FOR RASPBERRY PI ---
# 1. Make sure you have the original 'read_waveplus.py' script from the Airthings GitHub.
# 2. Place it in the same directory as this script.
# 3. Uncomment the line below:
# from read_waveplus import WavePlus
# 4. Replace the entire 'get_mock_data' function with the 'get_real_data' function provided below.
# -----------------------------------------

DB_NAME = "airthings.db"

def get_mock_data():
    """
    Generates fake sensor data for development on systems without Bluetooth/bluepy.
    This is the function you will replace on your Raspberry Pi.
    """
    print("Generating mock data...")
    return {
        'temperature': round(random.uniform(20.0, 25.0), 2),
        'humidity': round(random.uniform(30.0, 60.0), 2),
        'radon_short_term_avg': round(random.uniform(20.0, 80.0), 2),
        'radon_long_term_avg': round(random.uniform(20.0, 80.0), 2),
        'co2': round(random.uniform(400.0, 1000.0), 2),
        'voc': round(random.uniform(50.0, 300.0), 2),
    }

# --- FUNCTION TO USE ON RASPBERRY PI ---
# def get_real_data(sensor_serial_number):
#     """
#     Connects to the Airthings Wave Plus sensor and reads the real data.
#     """
#     print(f"Attempting to connect to sensor {sensor_serial_number}...")
#     try:
#         # NOTE: You will need to find your device's serial number and pass it here.
#         waveplus = WavePlus(sensor_serial_number)
#         sensors = waveplus.read()
#         print("Successfully read data from sensor.")
#         return {
#             'temperature': sensors.temperature,
#             'humidity': sensors.humidity,
#             'radon_short_term_avg': sensors.radon_short_term_avg,
#             'radon_long_term_avg': sensors.radon_long_term_avg,
#             'co2': sensors.co2,
#             'voc': sensors.voc,
#         }
#     except Exception as e:
#         print(f"ERROR: Failed to connect or read from the sensor. Reason: {e}")
#         return None
# -----------------------------------------

def insert_data(data):
    """Inserts a new data reading into the database."""
    if not data:
        print("No data to insert.")
        return

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO readings (temperature, humidity, radon_short_term_avg, radon_long_term_avg, co2, voc)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        data['temperature'],
        data['humidity'],
        data['radon_short_term_avg'],
        data['radon_long_term_avg'],
        data['co2'],
        data['voc']
    ))
    conn.commit()
    conn.close()
    print(f"Successfully inserted data into {DB_NAME}")

if __name__ == '__main__':
    # On your Mac, this will get mock data.
    # On the Pi, you will have modified this script to get real data.
    sensor_data = get_mock_data()

    # The rest of the script is the same for both environments.
    insert_data(sensor_data)
