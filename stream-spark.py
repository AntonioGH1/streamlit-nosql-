import streamlit as st
import requests
import pandas as pd
import json
import pymongo

# Inicializar conexión a MongoDB
@st.cache_resource
def init_mongo_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])

mongo_client = init_mongo_connection()

@st.cache_data(ttl=600)
def get_mongo_data():
    db = mongo_client.steam_db
    items = db.steam_games.find()
    return list(items)

# Inicializar conexión a PostgreSQL
conn = st.connection("postgresql", type="sql")

# Método para iniciar un trabajo de Spark en GitHub Actions
def post_spark_job(user, repo, job, token, codeurl, dataseturl):
    url = f'https://api.github.com/repos/{user}/{repo}/dispatches'
    payload = {
        "event_type": job,
        "client_payload": {"codeurl": codeurl, "dataseturl": dataseturl}
    }
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/vnd.github.v3+json',
        'Content-type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    st.write(response)

# Sidebar de la aplicación
st.sidebar.image('foto.png') 
st.sidebar.text("Antonio Rincon Villegas")
st.sidebar.text("zS21004480")
st.sidebar.text("Base de Datos No Convencionales")
st.sidebar.markdown("______")

# Contenido principal
st.title("Dashboard de Steam Games con Mongo y Postgre")

# Parámetros de GitHub Actions
github_user  = st.text_input('Usuario de Github', value='AntonioGH1')
github_repo  = st.text_input('Repositorio de Github', value='spark-labs')
spark_job    = st.text_input('Trabajo de Spark', value='spark')
github_token = st.text_input('Token de Github', value='*****')
code_url     = st.text_input('URL de Código', value='https://raw.githubusercontent.com/AntonioGH1/spark-labs/refs/heads/main/steam_games.py')
dataset_url  = st.text_input('URL de Dataset', value='https://raw.githubusercontent.com/AntonioGH1/kafka/refs/heads/main/games_data.csv')

if st.button("Ejecutar Spark Job"):
    post_spark_job(github_user, github_repo, spark_job, github_token, code_url, dataset_url)

st.markdown("____")

# Obtener resultados de Spark
def get_spark_results(url_results):
    response = requests.get(url_results)
    if response.status_code == 200:
        try:
            json_data = [json.loads(line) for line in response.text.strip().split("\n")]
            st.json(json_data)
        except json.JSONDecodeError as e:
            st.write("Error en JSON:", e)
            st.write(response.text)

st.header("Resultados de Spark")
url_results = st.text_input('URL de resultados', value='')
if st.button("Obtener Resultados de Spark"):
    get_spark_results(url_results)

st.markdown("____")

# Consulta de MongoDB
if st.sidebar.button("Consultar MongoDB"):
    items = get_mongo_data()
    st.header("Datos de MongoDB")
    if items:
        df_mongo = pd.DataFrame(items)
        st.dataframe(df_mongo)
    else:
        st.write("No hay datos en MongoDB")

st.markdown("____")

# Consulta de PostgreSQL
if st.sidebar.button("Consultar PostgreSQL"):
    st.header("Datos de PostgreSQL")
    df_pg = conn.query('SELECT * FROM steam_games;', ttl="10m")
    st.dataframe(df_pg)

st.sidebar.markdown("____")
