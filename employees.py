# Importar las librerías necesarias
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título de la aplicación
st.title('Análisis de Empleados')

# Descripción
st.write("___")

# Sidebar
sidebar = st.sidebar
#Logo
sidebar.markdown('<h3 style="text-align: center; color: red; font-weight: bold;">Antonio Rincon Villegas</h1>', unsafe_allow_html=True)
sidebar.markdown('<h3 style="text-align: center; font-weight: bold;">S21004480</h1>', unsafe_allow_html=True)

logo_path = "foto.png"
sidebar.image(logo_path, width=75)

# Cargar datos con cache
@st.cache_data
def load_data(nrows=None):
    """Carga el dataset de empleados."""
    try:
        data = pd.read_csv("Employees.csv", nrows=nrows, encoding="ISO-8859-1")
        return data
    except FileNotFoundError:
        st.error("El archivo 'Employees.csv' no se encontró. Verifica la ruta.")
        return pd.DataFrame()
    except UnicodeDecodeError:
        st.error("Error de decodificación. Verifica la codificación del archivo CSV.")
        return pd.DataFrame()

# Cargar datos completos
e_data_all = load_data()

# **Checkbox para mostrar/ocultar el DataFrame**
show_data = sidebar.checkbox("Mostrar todos los datos")

if show_data:
    st.write("### Datos completos de empleados")
    st.dataframe(e_data_all)

# **Buscador de empleados**
st.write("## Búsqueda de empleados")

col1, col2, col3 = st.columns(3)

with col1:
    search_id = st.text_input("Buscar por Employee_ID:")
with col2:
    search_hometown = st.text_input("Buscar por Hometown:")
with col3:
    search_unit = st.text_input("Buscar por Unit:")

if st.button("Buscar"):
    filtered_data = e_data_all
    if search_id:
        filtered_data = filtered_data[filtered_data['Employee_ID'].str.contains(search_id, case=False)]
    if search_hometown:
        filtered_data = filtered_data[filtered_data['Hometown'].str.contains(search_hometown, case=False)]
    if search_unit:
        filtered_data = filtered_data[filtered_data['Unit'].str.contains(search_unit, case=False)]

    st.write(f"### Resultados encontrados: {len(filtered_data)} empleados")
    st.dataframe(filtered_data)

# **Filtros en el Sidebar**
st.write("## Filtros adicionales")

# **Filtro por nivel educativo**
education_levels = e_data_all['Education_Level'].unique()
selected_education = sidebar.selectbox("Filtrar por nivel educativo:", ["Todos"] + list(map(str, education_levels)))

if selected_education != "Todos":
    filtered_edu = e_data_all[e_data_all['Education_Level'] == int(selected_education)]
    st.write(f"### Empleados con nivel educativo {selected_education}: {len(filtered_edu)}")
    st.dataframe(filtered_edu)

# **Filtro por ciudad**
hometowns = e_data_all['Hometown'].unique()
selected_hometown = sidebar.selectbox("Filtrar por ciudad:", ["Todas"] + list(hometowns))

if selected_hometown != "Todas":
    filtered_city = e_data_all[e_data_all['Hometown'] == selected_hometown]
    st.write(f"### Empleados en {selected_hometown}: {len(filtered_city)}")
    st.dataframe(filtered_city)

# **Filtro por unidad funcional (Unit)**
units = e_data_all['Unit'].unique()
selected_unit = sidebar.selectbox("Filtrar por unidad funcional:", ["Todas"] + list(units))

if selected_unit != "Todas":
    filtered_unit = e_data_all[e_data_all['Unit'] == selected_unit]
    st.write(f"### Empleados en {selected_unit}: {len(filtered_unit)}")
    st.dataframe(filtered_unit)

# **Gráficos**
st.write("## Análisis de datos")

# **Histograma de edades**
st.write("### Distribución de edades de los empleados")
fig, ax = plt.subplots(figsize=(8, 5))
ax.hist(e_data_all['Age'], bins=10, color='#007bff', edgecolor='black')
ax.set_xlabel("Edad")
ax.set_ylabel("Número de empleados")
ax.set_title("Distribución de empleados por edad")
st.pyplot(fig)

# **Frecuencia de empleados por unidad funcional**
st.write("### Frecuencia de empleados por Unidad")
unit_counts = e_data_all['Unit'].value_counts()
fig, ax = plt.subplots(figsize=(10, 5))
unit_counts.plot(kind="bar", color='purple', ax=ax)
ax.set_xlabel("Unidad Funcional")
ax.set_ylabel("Número de empleados")
ax.set_title("Empleados por Unidad")
st.pyplot(fig)

# **Ciudades con mayor índice de deserción**
st.write("### Ciudades con mayor índice de deserción")
attrition_by_city = e_data_all.groupby("Hometown")["Attrition_rate"].mean().sort_values(ascending=False)
fig, ax = plt.subplots(figsize=(10, 5))
attrition_by_city.plot(kind="bar", color="red", ax=ax)
ax.set_xlabel("Ciudad")
ax.set_ylabel("Tasa de deserción")
ax.set_title("Índice de deserción por ciudad")
st.pyplot(fig)

# **Edad vs. Tasa de deserción**
st.write("### Relación entre edad y tasa de deserción")
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(e_data_all["Age"], e_data_all["Attrition_rate"], color="green", alpha=0.5)
ax.set_xlabel("Edad")
ax.set_ylabel("Tasa de deserción")
ax.set_title("Edad vs. Tasa de deserción")
st.pyplot(fig)

# **Tiempo de servicio vs. Tasa de deserción**
st.write("### Relación entre tiempo de servicio y tasa de deserción")
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(e_data_all["Time_of_service"], e_data_all["Attrition_rate"], color="orange", alpha=0.5)
ax.set_xlabel("Años de servicio")
ax.set_ylabel("Tasa de deserción")
ax.set_title("Tiempo de servicio vs. Tasa de deserción")
st.pyplot(fig)

st.write("Fin del análisis.")
