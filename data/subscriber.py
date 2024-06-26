import paho.mqtt.client as mqtt
import json
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

# Initialize Firebase connection
cred = credentials.Certificate('./devsecopslbprojet-firebase-adminsdk-zhm7r-342dcd7ba6.json')  
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://devsecopslbprojet-default-rtdb.europe-west1.firebasedatabase.app/' 
})

# MQTT connection and message reception functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully with result code " + str(rc))
        client.subscribe("wokwi-weather")
    else:
        print("Failed to connect, return code " + str(rc))

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        print(f"Raw message payload: {payload}")  # Display raw message content
        if payload:
            data = json.loads(payload)
            print(f"Received message: ID: {data['id_capteur']}, Temperature: {data['temp']}°C, Humidity: {data['humidity']}%, Latitude: {data['position']['lat']}, Longitude: {data['position']['lon']}")
            
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            ref = db.reference('sensor_data')
            snapshot = ref.get()
            next_index = len(snapshot) if snapshot else 1
            ref.child(str(next_index)).set({
                'timestamp': timestamp,
                'temperature': data['temp'],
                'humidity': data['humidity'],
                'id_capteur': data['id_capteur'],
                'latitude': data['position']['lat'],
                'longitude': data['position']['lon']
            })
        else:
            print("Received an empty message")
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code " + str(rc))
    if rc != 0:
        print("Unexpected disconnection. Trying to reconnect...")
        try:
            client.reconnect()
        except Exception as e:
            print(f"Failed to reconnect: {e}")

def on_connect_fail(client, userdata, rc):
    print("Failed to connect with result code " + str(rc))

# Initialize MQTT client
client = mqtt.Client(protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.on_connect_fail = on_connect_fail

client.connect("broker.mqttdashboard.com", 1883, 60)

client.loop_forever()
