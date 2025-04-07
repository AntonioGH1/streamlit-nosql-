import streamlit as st
import requests
import pandas  as pd
import json
import pymongo

# Initialize connection. Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])
client = init_connection()
# Pull data from the collection. Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def get_data():
    db = client.people
    items = db.people.find()
    items = list(items)  # make hashable for st.cache_data
    return items
if st.button("Query mongodb collection"):
    items = get_data()

    # Print results.
    for item in items:
        st.write(item)
