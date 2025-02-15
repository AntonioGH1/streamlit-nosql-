import pandas as pd 

import streamlit as st  

names_link = 'dataset.csv'  
names_data = pd.read_csv(names_link)

###

@st.cache_data
def load_data():
    data = names_data
    return data
    #names_link = 'dataset.csv'
    #return pd.read_csv(names_link)

st.title("Streamlit and pandas")
# Cargar datos con caché
names_data = load_data()

###Grafico
def bienvenida(nombre):
    mymensaje = 'bienvenido/a: ' + nombre
    return mymensaje

myname = st.text_input('nombre :')
if (myname):
    mensaje = bienvenida(myname)
    st.write(f"Tu nombre es: {mensaje}")

#
name_query = st.text_input("Buscar nombre:", "")
if name_query:
    filtered_data = names_data[names_data['name'].str.startswith(name_query, na=False)]
else:
    filtered_data = names_data #Muestra todos

# Mostrar los datos filtrados
st.dataframe(filtered_data)

#st.dataframe(names_data)

