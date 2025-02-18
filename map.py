import pandas as pd
import numpy as np
import streamlit as st

st.title('Uber pickups in NYC')
#Logo
st.markdown('<h3 style="text-align: center; color: red; font-weight: bold;">Antonio</h1>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align: center; font-weight: bold;">S21004480</h1>', unsafe_allow_html=True)

logo_path = "foto.png"
st.image(logo_path, width=50)

DATE_COLUMN = 'date/time'
DATA_URL = ('uber_dataset.csv')
@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower() 
    data.rename(lowercase, axis='columns', inplace=True) 
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN]) 
    return data
data_load_state = st.text('Loading data...')
data = load_data(1000)
data_load_state.text("Done! (using st.cache)")
# Some number in the range 0-23
hour_to_filter = st.slider('hour', 0, 23, 17)
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)