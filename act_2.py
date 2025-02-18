import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Configuración de la app
st.title('Aplicación con Varias Pestañas')

sidebar = st.sidebar
#Logo
sidebar.markdown('<h3 style="text-align: center; color: red; font-weight: bold;">Antonio Rincon Villegas</h1>', unsafe_allow_html=True)
sidebar.markdown('<h3 style="text-align: center; font-weight: bold;">S21004480</h1>', unsafe_allow_html=True)

logo_path = "foto.png"
sidebar.image(logo_path, width=75)

# Crear las pestañas
tabs = st.tabs(["App 1", "App 2", "App 3", "App 4"])

# Pestaña 1: App 1
with tabs[0]:
    st.title('App 1')

    titanic_link = 'titanic.csv'
    titanic_data = pd.read_csv(titanic_link)

    st.header("Dataset")
    agree = st.checkbox("Mostrar Dataset Overview?")
    if agree:
        st.dataframe(titanic_data)

    # Selección de ciudad de embarque
    selected_town = st.radio("Seleccione ciudad de embarque:", titanic_data['embark_town'].dropna().unique())
    st.write("Ciudad seleccionada:", selected_town)
    st.write(titanic_data.query("embark_town == @selected_town"))

    st.markdown("___")

    # Filtros de tarifas
    optionals = st.expander("Opciones avanzadas", True)
    fare_min = optionals.slider("Tarifa mínima", float(titanic_data['fare'].min()), float(titanic_data['fare'].max()))
    fare_max = optionals.slider("Tarifa máxima", float(titanic_data['fare'].min()), float(titanic_data['fare'].max()))

    subset_fare = titanic_data[(titanic_data['fare'] <= fare_max) & (titanic_data['fare'] >= fare_min)]
    st.write(f"Registros con tarifas entre {fare_min} y {fare_max}: {subset_fare.shape[0]}")
    st.dataframe(subset_fare)

# Pestaña 2: App 2
with tabs[1]:
    st.title('App 2')

    titanic_link = "titanic.csv"
    titanic_data = pd.read_csv(titanic_link)

    st.header("Dataset del Titanic")
    st.dataframe(titanic_data)

    # Histograma de tarifas
    fig, ax = plt.subplots()
    ax.hist(titanic_data['fare'], bins=20, color='skyblue', edgecolor='black')
    st.header('Histograma - Fare')
    st.pyplot(fig)

    st.markdown("___")

    # Gráfico de barras: promedio de tarifas por clase
    fig2, ax2 = plt.subplots()
    avg_fare_per_class = titanic_data.groupby("class")["fare"].mean()
    ax2.barh(avg_fare_per_class.index, avg_fare_per_class.values, color='lightcoral')
    ax2.set_ylabel("Clase")
    ax2.set_xlabel("Tarifa promedio")
    ax2.set_title('¿Cuánto pagaron las clases del Titanic?')
    st.header("Gráfica de Barras del Titanic")
    st.pyplot(fig2)

    st.markdown("___")

    # Gráfico de dispersión: edad vs tarifa
    fig3, ax3 = plt.subplots()
    ax3.scatter(titanic_data['age'], titanic_data['fare'], alpha=0.5, color='green')
    ax3.set_xlabel("Edad")
    ax3.set_ylabel("Tarifa")
    st.header("Gráfica de Dispersión del Titanic")
    st.pyplot(fig3)

# Pestaña 3: App 3
with tabs[2]:
    st.title('App 3')

    # Mapa con coordenadas aleatorias centradas en San Francisco
    map_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
        columns=['lat', 'lon']
    )
    st.map(map_data)

# Pestaña 4: App 4
with tabs[3]:
    st.title('App 4')

    DATE_COLUMN = 'date/time'
    DATA_URL = 'uber_dataset.csv'

    @st.cache_data
    def load_data(nrows):
        data = pd.read_csv(DATA_URL, nrows=nrows)
        lowercase = lambda x: str(x).lower()
        data.rename(lowercase, axis='columns', inplace=True)
        data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
        return data

    data_load_state = st.text('Cargando datos...')
    data = load_data(1000)
    data_load_state.text("¡Datos cargados!")

    # Selección de hora para filtrar
    hour_to_filter = st.slider('Selecciona una hora:', 0, 23, 17)
    filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

    st.subheader(f'Mapa de viajes a las {hour_to_filter}:00')
    st.map(filtered_data)
