import streamlit as st
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.dates import DateFormatter

if not firebase_admin._apps:
    cred = credentials.Certificate('./devsecopslbprojet-firebase-adminsdk-zhm7r-342dcd7ba6.json')  
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://devsecopslbprojet-default-rtdb.europe-west1.firebasedatabase.app/' 
    })

def fetch_data():
    try:
        ref = db.reference('sensor_data')
        snapshot = ref.get()
        
        if snapshot is None:
            st.warning('No data found in Firebase.')
            return [], [], []
        
        timestamps = []
        temperatures = []
        humidities = []
        
        if isinstance(snapshot, list):
            for entry in snapshot:
                if entry is not None:
                    timestamps.append(entry.get('timestamp', ''))
                    temperatures.append(entry.get('temperature', ''))
                    humidities.append(entry.get('humidity', ''))
        else:
            st.warning('Unexpected data format returned from Firebase.')
            return [], [], []
        
        return timestamps, temperatures, humidities
    
    except Exception as e:
        st.error(f"Error fetching data from Firebase: {e}")
        return [], [], []

def compute_statistics(data):
    data = np.array(data, dtype=float)
    moyenne = np.mean(data)
    max_val = np.max(data)
    min_val = np.min(data)
    ecart_type = np.std(data)
    return moyenne, max_val, min_val, ecart_type

def filter_data_by_date(timestamps, data, start_date, end_date):
    filtered_data = [d for ts, d in zip(timestamps, data) if start_date <= ts <= end_date]
    return filtered_data

def main():
    st.title('Visualisation des données de température et d\'humidité')
    st.header('Visualisation des données de température et d\'humidité')
    
    timestamps, temperatures, humidities = fetch_data()
    
    if not timestamps:
        st.warning('Aucune donnée disponible à afficher.')
        return
    
    try:
        timestamps = [datetime.strptime(ts, '%Y-%m-%d %H:%M:%S') for ts in timestamps]
    except ValueError as ve:
        st.error(f"Erreur de conversion des timestamps: {ve}")
        return
    
    st.subheader('Température au fil du temps')
    fig_temp, ax_temp = plt.subplots()
    ax_temp.plot(timestamps, temperatures, marker='o', linestyle='-', color='b', label='Température (°C)')
    ax_temp.set_xlabel('Timestamp')
    ax_temp.set_ylabel('Température (°C)')
    ax_temp.grid(True)
    
    ax_temp.xaxis.set_major_formatter(DateFormatter('%M'))
    
    st.pyplot(fig_temp)
    
    st.subheader('Humidité au fil du temps')
    fig_humidity, ax_humidity = plt.subplots()
    ax_humidity.plot(timestamps, humidities, marker='o', linestyle='-', color='g', label='Humidité (%)')
    ax_humidity.set_xlabel('Timestamp')
    ax_humidity.set_ylabel('Humidité (%)')
    ax_humidity.grid(True)
    
    ax_humidity.xaxis.set_major_formatter(DateFormatter('%M'))
    
    st.pyplot(fig_humidity)
    
    st.subheader('Sélectionner la période pour les statistiques')
    start_date = st.date_input('Date de début', min(timestamps).date())
    end_date = st.date_input('Date de fin', max(timestamps).date())
    
    if start_date > end_date:
        st.error('La date de début doit être antérieure ou égale à la date de fin.')
        return
    
    if st.button('Afficher les statistiques'):
        filtered_temps = filter_data_by_date(timestamps, temperatures, datetime.combine(start_date, datetime.min.time()), datetime.combine(end_date, datetime.max.time()))
        filtered_humidities = filter_data_by_date(timestamps, humidities, datetime.combine(start_date, datetime.min.time()), datetime.combine(end_date, datetime.max.time()))
        
        if not filtered_temps or not filtered_humidities:
            st.warning('Aucune donnée disponible pour la période sélectionnée.')
            return
        
        st.subheader('Statistiques des températures')
        moyenne_temp, max_temp, min_temp, ecart_type_temp = compute_statistics(filtered_temps)
        st.write(f"Moyenne: {moyenne_temp:.2f} °C")
        st.write(f"Valeur maximale: {max_temp:.2f} °C")
        st.write(f"Valeur minimale: {min_temp:.2f} °C")
        st.write(f"Écart type: {ecart_type_temp:.2f}")
        
        st.subheader('Statistiques des humidités')
        moyenne_hum, max_hum, min_hum, ecart_type_hum = compute_statistics(filtered_humidities)
        st.write(f"Moyenne: {moyenne_hum:.2f} %")
        st.write(f"Valeur maximale: {max_hum:.2f} %")
        st.write(f"Valeur minimale: {min_hum:.2f} %")
        st.write(f"Écart type: {ecart_type_hum:.2f}")

if __name__ == '__main__':
    main()
