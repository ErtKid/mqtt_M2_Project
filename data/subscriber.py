import paho.mqtt.client as mqtt
import json
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

cred = credentials.Certificate('./devsecopslbprojet-firebase-adminsdk-zhm7r-342dcd7ba6.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://devsecopslbprojet-default-rtdb.europe-west1.firebasedatabase.app/'
})

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully with result code " + str(rc))
        client.subscribe("wokwi-weather", qos=1)
    else:
        print("Failed to connect, return code " + str(rc))

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode('utf-8')
        print(f"Raw message payload: {payload}")
        if payload:
            data = json.loads(payload)
            print(f"Received message: Temperature: {data['temp']}°C, Humidity: {data['humidity']}%")

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            ref = db.reference('sensor_data')
            # Vérifier les doublons avant d'ajouter les nouvelles données
            snapshot = ref.order_by_child('timestamp').equal_to(timestamp).get()
            if snapshot:
                print("Duplicate data detected, not storing to Firebase.")
                return

            ref.push({
                'timestamp': timestamp,
                'temperature': data['temp'],
                'humidity': data['humidity'],
                'location': data['position']
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

client = mqtt.Client(protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_message = on_message
client.on_disconnect = on_disconnect
client.on_connect_fail = on_connect_fail

client.connect("broker.mqttdashboard.com", 1883, 60)

client.loop_forever()
