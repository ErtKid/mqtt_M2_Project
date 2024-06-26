import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import matplotlib.pyplot as plt

if not firebase_admin._apps:
    cred = credentials.Certificate('./devsecopslbprojet-firebase-adminsdk-zhm7r-342dcd7ba6.json')  
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://devsecopslbprojet-default-rtdb.europe-west1.firebasedatabase.app/' 
    })

# Function to fetch data from Firebase
def fetch_data():
    try:
        ref = db.reference('sensor_data')
        snapshot = ref.get()
        
        if not snapshot:
            st.warning('No data found in Firebase.')
            return [], [], []
        
        timestamps = []
        temperatures = []
        humidities = []
        
        if isinstance(snapshot, list):
            # Handle case where snapshot is a list of entries
            for entry in snapshot:
                timestamps.append(entry.get('timestamp', ''))
                temperatures.append(entry.get('temp', ''))
                humidities.append(entry.get('humidity', ''))
        elif isinstance(snapshot, dict):
            # Handle case where snapshot is a dictionary of entries
            for key, data_point in snapshot.items():
                timestamps.append(data_point.get('timestamp', ''))
                temperatures.append(data_point.get('temp', ''))
                humidities.append(data_point.get('humidity', ''))
        else:
            st.warning('Unexpected data format returned from Firebase.')
            return [], [], []
        
        return timestamps, temperatures, humidities
    
    except Exception as e:
        st.error(f"Error fetching data from Firebase: {e}")
        return [], [], []

# Main Streamlit app
def main():
    st.title('Temperature and Humidity Data Visualization')
    st.header('Temperature and Humidity Data Visualization')
    
    # Fetch data from Firebase
    timestamps, temperatures, humidities = fetch_data()
    
    if not timestamps:
        st.warning('No data available to display.')
        return
    
    # Convert timestamps to datetime objects for plotting
    timestamps = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in timestamps]
    
    # Plotting temperature graph
    st.subheader('Temperature Over Time')
    fig_temp, ax_temp = plt.subplots()
    ax_temp.plot(timestamps, temperatures, marker='o', linestyle='-', color='b', label='Temperature (°C)')
    ax_temp.set_xlabel('Timestamp')
    ax_temp.set_ylabel('Temperature (°C)')
    ax_temp.grid(True)
    
    # Display temperature plot in Streamlit
    st.pyplot(fig_temp)
    
    # Plotting humidity graph
    st.subheader('Humidity Over Time')
    fig_humidity, ax_humidity = plt.subplots()
    ax_humidity.plot(timestamps, humidities, marker='o', linestyle='-', color='g', label='Humidity (%)')
    ax_humidity.set_xlabel('Timestamp')
    ax_humidity.set_ylabel('Humidity (%)')
    ax_humidity.grid(True)
    
    # Display humidity plot in Streamlit
    st.pyplot(fig_humidity)

if __name__ == '__main__':
    main()
