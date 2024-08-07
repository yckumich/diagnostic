import streamlit as st

#----------------------INIT-----------------------
st.set_page_config(
    page_title="Custom Condition Tier",
    layout="wide",
    initial_sidebar_state="expanded"
)

import pandas as pd
from utils.condition_tier_utils.utils import *

def initialize_session_state():
    if "custom_condition_list" not in st.session_state:
        st.session_state.custom_condition_list = []

    if "custom_condition_df" not in st.session_state:
        st.session_state.custom_condition_df = None

    if 'show_plot' not in st.session_state:
        st.session_state['show_plot'] = False

initialize_session_state()

GDB_CONDITION_LIST = retrieve_gbd_conditions()

#----------------------MAIN-----------------------
add_sidebar()
build_col, display_col = st.columns([1,1], gap="small")
    
with build_col:
    st.write("### Custom Condition Tier Table")
    # Display the current condition data
    display_custom_condition_df()

    _, col_1, col_2, _ = st.columns([0.2, 0.3, 0.3, 0.2])
    with col_1:
        delete_current_coustom_df()
    with col_2:
        save_current_coustom_df()

    # Form to add a new condition
    display_add_condition_form()
    upload_custom_condition_csv()


with display_col:
    if len(st.session_state["custom_condition_list"]) > 1:
        if not st.session_state['show_plot']:
            st.markdown("""<div style="height:500px;"></div>""", unsafe_allow_html=True)
            _, col, _ = st.columns([0.35, 0.3, 0.35])
            with col:
                if st.button('Render Custom Condition Tier Plot'):
                    st.session_state['show_plot'] = True
                    st.rerun()
        else:
            render_plot()
    else:
        st.markdown("""<div style="height:400px;"></div>""", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Must build/upload custom condition tier dataframe to render the plot</h2>", unsafe_allow_html=True)
