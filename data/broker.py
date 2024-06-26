import time
import json
import random
import paho.mqtt.client as mqtt

# MQTT Server Parameters
MQTT_CLIENT_ID = "sensor-simulator-1" # Identifiant unique du client
MQTT_BROKER = "broker.mqttdashboard.com"
MQTT_TOPIC = "wokwi-weather"

# Position du capteur (exemple : latitude et longitude)
CAPTEUR_POSITION = {"lat": 48.8566, "lon": 2.3522}  # Paris, France

# Fonction pour simuler la mesure du capteur
def measure():
    return {
        "id_capteur": MQTT_CLIENT_ID,
        "position": CAPTEUR_POSITION,
        "temp": round(random.uniform(20.0, 30.0), 2),  # Température entre 20 et 30 degrés Celsius
        "humidity": round(random.uniform(30.0, 60.0), 2),  # Humidité entre 30% et 60%
        "timestamp": time.time()
    }

print("Connecting to MQTT server... ", end="")
client = mqtt.Client(client_id=MQTT_CLIENT_ID, protocol=mqtt.MQTTv311)
client.connect(MQTT_BROKER)
print("Connected!")

prev_weather = ""
while True:
    weather = measure()
    message = json.dumps(weather)
    if message != prev_weather:
        print("Updated!")
        print(f"Reporting to MQTT topic {MQTT_TOPIC}: {message}")
        client.publish(MQTT_TOPIC, message, qos=1)  # Utilisation de QoS 1 pour eviter les doublons
        prev_weather = message
    else:
        print("No change")
    time.sleep(5)
