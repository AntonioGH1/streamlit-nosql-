import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título de la aplicación
st.title("CitiBike")

sidebar = st.sidebar

#Logo
sidebar.markdown('<h3 style="text-align: center; color: red; font-weight: bold;">Antonio Rincon Villegas</h1>', unsafe_allow_html=True)
sidebar.markdown('<h3 style="text-align: center; font-weight: bold;">S21004480</h1>', unsafe_allow_html=True)

logo_path = "foto.png"
sidebar.image(logo_path, width=75)


# Cargar datos con cache
@st.cache_data
def load_data(nrows=None):
    """Carga el dataset de CitiBike y devuelve un DataFrame con el número de registros solicitados."""
    try:
        data = pd.read_csv("citibike-tripdata.csv", nrows=nrows, encoding="ISO-8859-1")
        data['started_at'] = pd.to_datetime(data['started_at'], errors='coerce')  # Convertir a datetime
        data['hour'] = data['started_at'].dt.hour  # Extraer la hora
        return data
    except (FileNotFoundError, UnicodeDecodeError) as e:
        st.error(f"Error al cargar datos: {e}")
        return pd.DataFrame()

# **Checkbox para mostrar todos los datos**
show_all = sidebar.checkbox("Mostrar todos los registros")

# Cargar datos según el checkbox
if show_all:
    bikes_data = load_data(None)  # Cargar todos los datos
else:
    bikes_data = load_data(500)   # Solo 500 registros

# **Restaurar el índice original sin reiniciar**
bikes_data.reset_index(drop=False, inplace=True)

# **Slider para seleccionar la hora**
hour = sidebar.slider("Selecciona la hora del día (0-23):", 0, 23, 12)

# **Filtrar datos por la hora seleccionada**
filtered_data = bikes_data[bikes_data['hour'] == hour]

# **Renombrar columnas para el mapa**
filtered_data = filtered_data.rename(columns={"start_lat": "lat", "start_lng": "lon"})

# **Mostrar DataFrame según el checkbox y la hora**
st.write(f"### Registros a las {hour}:00 horas")
st.write(f"Se están mostrando {'todos' if show_all else '500'} registros filtrados por hora.")
st.dataframe(bikes_data)

# **Gráfica de barras por hora**
st.write("### 🚲 Número total de recorridos por hora")
hourly_counts = bikes_data['hour'].value_counts().sort_index()

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(hourly_counts.index, hourly_counts.values, color='#007bff')
ax.set_xlabel('Hora del día')
ax.set_ylabel('Número de recorridos')
ax.set_title('Número total de recorridos por hora del día')
ax.set_xticks(range(0, 24))
ax.grid(True, linestyle='--', alpha=0.7)

st.pyplot(fig)

# **Mapa con puntos GPS**
st.write(f"### 🗺️ Mapa de recorridos a las {hour}:00 horas")
if not filtered_data.empty:
    st.map(filtered_data[['lat', 'lon']])
else:
    st.write(f"No hay recorridos iniciados a las {hour}:00 horas.")

# Fin del visor
st.write("Fin del visor de CitiBike.")
