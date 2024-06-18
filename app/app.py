import streamlit as st
from sqlalchemy.orm import Session
from data.database import get_db
from data.models import *  # Replace with your actual model

# Streamlit app
st.title('Database Viewer')

# Function to fetch data from the database
def fetch_data():
    with next(get_db()) as db:
        results = db.query(t_tableau3_t2_tjfs_join_edl_dashadmin).limit(2).all()  # Replace with your actual query
        return results

# Display data in Streamlit
data = fetch_data()
st.write(data)