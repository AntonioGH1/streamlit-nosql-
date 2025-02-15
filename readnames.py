import pandas as pd
import streamlit as st

# Función para cargar los datos con caché
@st.cache_data
def load_data():
    return pd.read_csv('dataset.csv')

# Título de la app
st.title("Buscador de Nombres")

# Cargar datos
names_data = load_data()
# Asegurarse de que 'index' sea un valor numérico
names_data['index'] = pd.to_numeric(names_data['index'], errors='coerce')

# Inputs para definir el rango de búsqueda
start_name = st.text_input("Nombre inicial:")
end_name = st.text_input("Nombre final:")
index_name = st.text_input("Numero a buscar: ")

# Botón para ejecutar la búsqueda
if st.button("Buscar"):
    if start_name and end_name:
        filtered_data = names_data[
            (names_data['name'] >= start_name) & (names_data['name'] <= end_name)
        ]
        st.write(f"Mostrando nombres entre **{start_name}** y **{end_name}**")
        st.dataframe(filtered_data)
    else:
        st.warning("Por favor, ingresa ambos nombres para definir el rango.")

# Botón para ejecutar la búsqueda por número
if st.button("Numero"):
    if index_name:
        try:
            index_name = int(index_name)  # Convertir el input a número
            filtered_data = names_data[
                names_data['index'] >= index_name
            ]
            st.write(f"Mostrando nombres con número mayor o igual a **{index_name}**")
            st.dataframe(filtered_data)
        except ValueError:
            st.warning("Por favor, ingresa un número válido.")
    else:
        st.warning("Por favor, ingresa un número para buscar.")

st.dataframe(names_data)