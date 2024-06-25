import time
import json
import random
import paho.mqtt.client as mqtt

# MQTT Server Parameters
MQTT_CLIENT_ID = "sensor-simulator"
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC = "wokwi-weather"

# Fonction pour simuler la mesure du capteur
def measure():
    return {
        "temp": round(random.uniform(20.0, 30.0), 2),  # Température entre 20 et 30 degrés Celsius
        "humidity": round(random.uniform(30.0, 60.0), 2),  # Humidité entre 30% et 60%
    }

print("Connecting to MQTT server... ", end="")
client = mqtt.Client(client_id=MQTT_CLIENT_ID, protocol=mqtt.MQTTv311)  # Utilisation de MQTTv311
client.connect(MQTT_BROKER)
print("Connected!")

prev_weather = ""
while True:
    weather = measure()
    message = json.dumps(weather)
    if message != prev_weather:
        print("Updated!")
        print(f"Reporting to MQTT topic {MQTT_TOPIC}: {message}")
        client.publish(MQTT_TOPIC, message)
        prev_weather = message
    else:
        print("No change")
    time.sleep(5)
