import os
import sqlite3
import threading
from datetime import datetime
from flask import Flask, jsonify, render_template
import paho.mqtt.client as mqtt

app = Flask(__name__)

MQTT_BROKER = os.environ.get("MQTT_BROKER", "localhost")
MQTT_PORT = 1883
TOPIC = "sensor/humidity"
DB_PATH = os.path.join(os.path.dirname(__file__), "plant.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            humidity INTEGER NOT NULL,
            time TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_reading(humidity):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO readings (humidity, time) VALUES (?, ?)", (humidity, timestamp))
    conn.commit()
    conn.close()

def get_last_readings():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT humidity, time FROM readings ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [{"humidity": row[0], "time": row[1]} for row in reversed(rows)]

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to MQTT broker with result code {reason_code}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    try:
        humidity = int(msg.payload.decode())
        print(f"Received humidity: {humidity}")
        save_reading(humidity)
    except ValueError as e:
        print(f"Error parsing message: {e}")

def start_mqtt():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message

    while True:
        try:
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            break
        except Exception as e:
            print(f"MQTT connection failed: {e}, retrying in 5 seconds...")
            import time
            time.sleep(5)

    client.loop_forever()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/data")
def data():
    readings = get_last_readings()
    return jsonify(readings)

if __name__ == "__main__":
    init_db()

    mqtt_thread = threading.Thread(target=start_mqtt, daemon=True)
    mqtt_thread.start()

    app.run(host="0.0.0.0", port=5000)
