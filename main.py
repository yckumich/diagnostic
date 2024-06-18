import streamlit as st
from sqlalchemy.orm import Session
from data.database import engine, Base
from data.models import *  
from utils.utils import *
import pandas as pd

# Create the database tables (if they don't already exist)
Base.metadata.create_all(bind=engine)

def create_expander(expander_title, subfilter_map):
    selected_option_map = {k:[] for k in subfilter_map.keys()}
    with st.expander(expander_title):
        for subfilter_title, options_list in subfilter_map.items():
            selected_option_map[subfilter_title] = st.multiselect(subfilter_title, options_list, default=[])
    return {expander_title: selected_option_map}


def add_sidebar(filter_map):
    with st.sidebar:
        print(" ")
        st.header('Filters')
        for main_filter in filter_map:
            selected_option_map = create_expander(main_filter, filter_map[main_filter])
            print(selected_option_map)
        print(" ")

def main():
    st.set_page_config(
        page_title="EDL Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    filter_map = get_filter()
    add_sidebar(filter_map=filter_map)


if __name__ == "__main__":
    main()