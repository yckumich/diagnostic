import streamlit as st
from sqlalchemy.orm import Session
from data.database import engine, Base
from data.models import t_tableau3_t2_tjfs_join_edl_dashadmin
from utils.utils import *
import pandas as pd
from typing import Dict
from st_aggrid import AgGrid


# Create the database tables (if they don't already exist)
Base.metadata.create_all(bind=engine)
agg_filter_selection = dict()


def create_expander(expander_title:str, subfilter_map:dict) -> Dict:
    selected_option_map = {k:[] for k in subfilter_map.keys()}
    with st.expander(expander_title):
        for subfilter_title, options_list in subfilter_map.items():
            selected_option_map[subfilter_title] = st.multiselect(subfilter_title, options_list, default=[])
    return selected_option_map


def add_sidebar(filter_map):
    with st.sidebar:
        st.header('Filters')
        for main_filter in filter_map:
            # selected_option_map = create_expander(main_filter, filter_map[main_filter])
            agg_filter_selection[main_filter] = create_expander(main_filter, filter_map[main_filter])
    
    return agg_filter_selection


def display_test_details(test_details):
    for key, value in test_details.items():
        st.write(f"**{key}**: {value}")


def main():
    st.set_page_config(
        page_title="EDL Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    filter_map = get_filter()
    selection = add_sidebar(filter_map=filter_map)
    test_df = convert_selection_to_df(selection) #.drop_duplicates(subset=['testname']).reset_index(drop=True).sort_values(by='testname')
    # st.dataframe(test_df)
    AgGrid(test_df)

    # # If no test is selected, initialize session state
    # if 'selected_test' not in st.session_state:
    #     st.session_state['selected_test'] = None
    
    # # Layout with two columns
    # test_name_col, test_detail_col = st.columns([0.3, 0.7], gap="small")
    
    # # Display test names in col1
    # with test_name_col:
    #     st.header("Test Names")
    #     AgGrid(test_df[['testname']])


    # print(st.session_state['selected_test'])
    # Display test details in col2 if a test is selected
    # with col2:
    #     if st.session_state['selected_test']:
    #         st.header(f"Details for {st.session_state['selected_test']['testname']}")
    #         display_test_details(st.session_state['selected_test'])
    #     else:
    #         st.write("Select a test to see details.")


if __name__ == "__main__":
    main()