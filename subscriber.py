import paho.mqtt.client as mqtt
import json

# Fonction de connexion MQTT et de réception de message
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))
    client.subscribe("wokwi-weather")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        print(f"Raw message payload: {payload}")  # Afficher le contenu brut du message
        if payload:
            data = json.loads(payload)
            print(f"Received message: Temperature: {data['temp']}°C, Humidity: {data['humidity']}%")
        else:
            print("Received an empty message")
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

client = mqtt.Client(protocol=mqtt.MQTTv311)  # Utilisation de MQTTv311
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.mqttdashboard.com", 1883, 60)

client.loop_forever()
