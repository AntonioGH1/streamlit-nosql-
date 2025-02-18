import pandas as pd
import streamlit as st
import datetime
import matplotlib.pyplot as ptl

titanic_link = "titanic.csv"
titanic_data = pd.read_csv(titanic_link)

st.title('App Titanic')
sidebar = st.sidebar
#Logo
sidebar.markdown('<h3 style="text-align: center; color: red; font-weight: bold;">Antonio</h1>', unsafe_allow_html=True)
sidebar.markdown('<h3 style="text-align: center; font-weight: bold;">S21004480</h1>', unsafe_allow_html=True)

logo_path = "foto.png"
sidebar.image(logo_path, width=75)


today = datetime.date.today()
today_date = sidebar.date_input('Current Date', today)

st.dataframe(titanic_data)
st.header("Data Description")

#
fig, ax = ptl.subplots()
#Cambiar de fare a graph, no se
ax.hist(titanic_data.fare)
st.header('Histograma - Fare')
st.pyplot(fig)

st.markdown("___")

##
fig2, ax2 = ptl.subplots()
y_pos = titanic_data['class']
x_pos = titanic_data['fare']
ax2.barh(y_pos, x_pos)
ax2.set_ylabel("Class")
ax2.set_xlabel("Fare")
ax2.set_title('¿Cuanto pagaron las clases del Titanic')
st.header("Grafica de Barras del Titanic")
st.pyplot(fig2)

st.markdown("___")

###
fig3, ax3 = ptl.subplots()
ax3.scatter(titanic_data.age, titanic_data.fare)
ax3.set_xlabel("Edad")
ax3.set_ylabel("Tarifa")
st.header("Grafica de Dispersión del Titanic")
st.pyplot(fig3)