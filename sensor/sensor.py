import os
import time
import random
import paho.mqtt.client as mqtt

MQTT_BROKER = os.environ.get("MQTT_BROKER", "localhost")
MQTT_PORT = 1883
TOPIC = "sensor/humidity"

def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

    while True:
        try:
            client.connect(MQTT_BROKER, MQTT_PORT, 60)
            print(f"Connected to MQTT broker at {MQTT_BROKER}")
            break
        except Exception as e:
            print(f"Connection failed: {e}, retrying in 5 seconds...")
            time.sleep(5)

    client.loop_start()

    while True:
        humidity = random.randint(10, 90)
        client.publish(TOPIC, humidity)
        print(f"Published humidity: {humidity}")
        time.sleep(10)

if __name__ == "__main__":
    main()
