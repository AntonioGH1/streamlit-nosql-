import pandas as pd
import streamlit as st
import numpy as np

st.header("Mapa de San Francisco")
map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon']
    )
st.map(map_data)