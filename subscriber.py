import paho.mqtt.client as mqtt
import json
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
cred = credentials.Certificate('./devsecopslbprojet-firebase-adminsdk-zhm7r-e29a950853.json')  # Replace with the path to your Firebase credentials JSON file
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://devsecopslbprojet-default-rtdb.europe-west1.firebasedatabase.app/'  # Replace with your Firebase Realtime Database URL
})

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
            
            # Push data to Firebase
            ref = db.reference('sensor_data')
            ref.push({
                'temperature': data['temp'],
                'humidity': data['humidity']
            })
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
