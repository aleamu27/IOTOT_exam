import sqlite3
import datetime
from flask import Flask, render_template, request
import paho.mqtt.client as mqtt

#Init SQlite DB 
def startdb(
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS ganjabase (
            id INTEGER PRIMARY KEY,
            topic TEXT,
            moisture REAL, 
            timestamp DATETIME
            )
            ''')
            db.commit()

        def log_to_db(topic, moisture): 
            try: 
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            query = "INSERT INTO ganjabase (topic, moisture, timestamp) VALUES (?, ?, ?)"
values = (topic, moisture, current_time)
            cursor.execute(query, values)
            db.commit()
except Exception as e:
            print(f"Error: {str(e)}")

            #flask App
            app = Flask(_name_)

            @app.route('/')
            def index():
            page = request.args.get('page', 1, type=int)
            limit = 10
            offset = (page - 1) * limit
    date_filter = request.args.get('date')
    if date_filter:
        query = "SELECT * FROM ganjabase WHERE DATE(timestamp) = ? LIMIT ? OFFSET ?"
        total_query = "SELECT COUNT(*) FROM ganjabase WHERE DATE(timestamp) = ?"
        cursor.execute(total_query, (date_filter,))
        total_pages = (cursor.fetchone()[0] + limit - 1) // limit
        cursor.execute(query, (date_filter, limit, offset))
    else:
        cursor.execute("SELECT COUNT(*) FROM ganjabase")
        total_pages = (cursor.fetchone()[0] + limit - 1) // limit
        cursor.execute("SELECT * FROM ganjabase LIMIT ? OFFSET ?", (limit, offset))
    data = cursor.fetchall()
    return render_template('index.html', data=data, page=page, total_pages=total_pages, date_filter=date_filter)

# MQTT Settings and Connection
MQTT_BROKER = "192.168.220.1"
MQTT_PORT = 1883
MQTT_TOPIC = "plant/moisture"

def on_connect(client, userdata, flags, properties=None):
    print("Connected to MQTT Broker!")
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
    log_to_db(msg.topic, msg.payload.decode())

# SQLite Connection
db = sqlite3.connect('ganjabase.db', check_same_thread=False)
cursor = db.cursor()

# MQTT Client Setup
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# Initialize and Run
startdb()

if __name__ == '__main__':
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start()
        app.run(debug=True)
    except Exception as e:
        print(f"Error: {str(e)}")
        client.loop_stop()
