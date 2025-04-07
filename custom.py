import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title("Steam")

sidebar = st.sidebar
#Logo
sidebar.markdown('<h3 style="text-align: center; color: red; font-weight: bold;">Antonio Rincon Villegas</h1>', unsafe_allow_html=True)
sidebar.markdown('<h3 style="text-align: center; font-weight: bold;">S21004480</h1>', unsafe_allow_html=True)

logo_path = "foto.png"
sidebar.image(logo_path, width=75)


@st.cache_data
def load_data(nrows=None):
    """Carga el dataset de empleados."""
    try:
        data = pd.read_csv("games_data.csv", nrows=nrows, encoding="ISO-8859-1")
        return data
    except FileNotFoundError:
        st.error("El archivo 'games_data.csv' no se encontró. Verifica la ruta.")
        return pd.DataFrame()
    except UnicodeDecodeError:
        st.error("Error de decodificación. Verifica la codificación del archivo CSV.")
        return pd.DataFrame()

d_data_all = load_data()

# Entrada para definir el número de lanzamientos a recuperar
num = st.number_input("Número de lanzamientos a mostrar:", min_value=1, value=500)

#
# **Buscador de nombres**
st.write("## Búsqueda de juegos")

col1, col2, col3 = st.columns(3)

with col1:
    search_t = st.text_input("Buscar por Titulo:")
with col2:
    search_d = st.text_input("Buscar por Desarrollador:")
with col3:
    search_p = st.text_input("Buscar por Publicador:")

if st.button("Buscar"):
    filtered_data = d_data_all
    # Reemplazar NaN por cadena vacía en las columnas de búsqueda
    filtered_data[['title', 'developer', 'publisher']] = filtered_data[['title', 'developer', 'publisher']].fillna("")
    if search_t:
        filtered_data = filtered_data[filtered_data['title'].str.contains(search_t, case=False)]
    if search_d:
        filtered_data = filtered_data[filtered_data['developer'].str.contains(search_d, case=False)]
    if search_p:
        filtered_data = filtered_data[filtered_data['publisher'].str.contains(search_p, case=False)]

    st.write(f"### Resultados encontrados: {len(filtered_data)} Steam")
    st.dataframe(filtered_data)

# Checkbox para mostrar/ocultar el DataFrame Completo
show_data = sidebar.checkbox("Mostrar todos los datos")

if show_data:
    d_data_all = load_data(None)
    st.write(f"Cargando {len(d_data_all)} registros del dataset...")
else:
    d_data_all = load_data(num)
    st.write(f"Cargando {len(d_data_all)} registros del dataset...")

# Actualizar
d_data_all.reset_index(drop=False, inplace=True)
# Mostrar
st.dataframe(d_data_all)


# **Gráficos**
st.write("## Análisis de datos")

# Corregir conversión de fechas a años
d_data_all['year'] = pd.to_datetime(d_data_all['release_date'], errors='coerce').dt.year

# Eliminar registros con años inválidos (NaN o 0)
d_data_all = d_data_all[d_data_all['year'] > 0]

# Convertir a int después de limpiar
d_data_all['year'] = d_data_all['year'].astype(int)

##Histograma de años
st.write("### Distribución de ventas")
fig, ax = plt.subplots(figsize=(10, 6))
ax.hist(d_data_all['year'], bins=10, color='#007bff', edgecolor='black')
ax.set_title("Histograma de los Años con lanzamiento")
ax.set_xlabel("Año")
ax.set_ylabel("Lanzamientos")
# Mejorar la visibilidad de las etiquetas del eje X
plt.xticks(rotation=45, ha='right')  # Rotar las etiquetas del eje X
st.pyplot(fig)


st.write("## Filtrado de Juegos")

# Filtro por género con multiselect
selected_genres = st.multiselect("Selecciona Género(s):", d_data_all['genres'].dropna().unique())

# Filtro por año de lanzamiento con selectbox (sin valor por defecto)
selected_year = st.selectbox("Selecciona Año de Lanzamiento:", sorted(d_data_all['year'].unique()), index=None)

# Aplicar filtros
filtered_data = d_data_all.copy()

# Asegúrate de que los géneros sean listas antes de hacer el filtro
d_data_all['genres'] = d_data_all['genres'].apply(lambda x: x.split(";") if isinstance(x, str) else [])

if selected_genres:
    filtered_data = filtered_data[filtered_data['genres'].apply(lambda x: any(genre in x for genre in selected_genres))]

if selected_year:
    filtered_data = filtered_data[filtered_data['year'] == selected_year]

# Mostrar resultados filtrados
st.write(f"### Resultados encontrados: {len(filtered_data)} juegos")
st.dataframe(filtered_data)


#Gráfica de Barras: Cantidad de juegos por género**
st.write("Cantidad de juegos por género")
#Dividir los géneros en una lista (porque están separados por ";")
d_data_all['genres'] = d_data_all['genres'].astype(str).str.split(";")
#Expandir la lista de géneros en filas separadas
df_exploded = d_data_all.explode('genres')
#Contar juegos por género. Limitar a 10
genre_counts = df_exploded['genres'].value_counts().head(10)
#
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(genre_counts.index, genre_counts.values, color='blue', edgecolor='black')
# Etiquetas y título
ax.set_title("Cantidad de juegos por género")
ax.set_xlabel("Género")
ax.set_ylabel("Cantidad de Juegos")
plt.xticks(rotation=45, ha="right")  # Rotar etiquetas del eje X para mejor visualización
st.pyplot(fig)


##Gráfica Scatter: Relación entre Precio y Reseñas
st.write("Relación entre el precio y la cantidad de reseñas")
# Convertir la columna 'price' a valores numéricos (eliminando texto como 'Free to Play')
d_data_all['price'] = pd.to_numeric(d_data_all['price'], errors='coerce')
d_data_all['reviews'] = pd.to_numeric(d_data_all['reviews'], errors='coerce')
# Filtrar datos válidos (descartar NaN)
df_filtered = d_data_all.dropna(subset=['price', 'reviews'])

# Crear la gráfica de dispersión
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(df_filtered['price'], df_filtered['reviews'], alpha=0.5, color='red')

# Etiquetas y título
ax.set_title("Relación entre Precio y Número de Reseñas")
ax.set_xlabel("Precio del Juego (USD)")
ax.set_ylabel("Número de Reseñas")
# Mostrar la gráfica en Streamlit
st.pyplot(fig)

st.write("Nuevo Scatter")

win = d_data_all[d_data_all['win_support'] == 1]['reviews']
mac = d_data_all[d_data_all['mac_support'] == 1]['reviews']
linux = d_data_all[d_data_all['lin_support'] == 1]['reviews']

# Crear el scatter plot
fig, ax = plt.subplots(figsize=(8, 6))
ax.scatter([1] * len(win), win, color='blue', label='Windows', alpha=0.6)
ax.scatter([2] * len(mac), mac, color='green', label='Mac', alpha=0.6)
ax.scatter([3] * len(linux), linux, color='red', label='Linux', alpha=0.6)

# Configurar etiquetas y diseño
ax.set_xticks([1, 2, 3])
ax.set_xticklabels(['Windows', 'Mac', 'Linux'])
ax.set_xlabel("Sistema Operativo")
ax.set_ylabel("Cantidad de Reseñas")
ax.set_title("Cantidad de Reseñas por Compatibilidad con Sistemas Operativos")
ax.legend()
ax.grid(True, alpha=0.5)

# Mostrar gráfico en Streamlit
st.pyplot(fig)
