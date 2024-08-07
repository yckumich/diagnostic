import pandas as pd
from utils.tests_summary_utils.utils import *
# from utils.dataframe_utils.utils import convert_selection_to_df
# from utils.dataframe_utils.utils_center_tab import get_lab_specific_test_by_laboratory_section
from utils.test_tier_utils.utils import *
from utils.condition_tier_utils.utils import *


from style import get_style_markdown
import streamlit as st
import time
from typing import List

#----------------------INIT-----------------------
st.set_page_config(
    page_title="Diagnostic Test Summary",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

get_style_markdown()

if "display_test_summary" not in st.session_state:
    st.session_state.display_test_summary = False

if "test_summary_df" not in st.session_state:
    st.session_state.test_summary_df = None

if "curr_clstbls_list" not in st.session_state:
    st.session_state.curr_clstbls_list = None

if "custom_condition_list" not in st.session_state:
    st.session_state.custom_condition_list = []

if "custom_test_tier_list" not in st.session_state:
    st.session_state.custom_test_tier_list = []

if "inline_custom_condition_list" not in st.session_state:
    st.session_state.inline_custom_condition_list = []

if "inline_custom_test_list" not in st.session_state:
    st.session_state.inline_custom_test_list = []


#----------------------MAIN-----------------------
# add_sidebar()
st.write("### Test Summary")
build_col, display_col = st.columns([1, 1], gap="medium")

with build_col:
    (custom_cond_tier_tab, 
     custom_test_tier_tab,)  = st.tabs([
         'Custom Condition Tier', 
         'Custom Test Tier', 
         ])

    with custom_cond_tier_tab:
        if len(st.session_state.custom_condition_list) == 0:
            st.markdown("""<div style="height:400px;"></div>""", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: grey;'>Must create/upload custom condition tier (Check instruction on the page 3)</h2>", unsafe_allow_html=True)
        else:
            st.session_state.inline_custom_condition_list = st.session_state.custom_condition_list.copy()
            inline_display_custom_condition_df()

            _, col_0, col_1, col_2, _ = st.columns([0.125, 0.25, 0.25, 0.25, 0.125])
            with col_0:
                inline_fetch_custom_condition_tier() 
            with col_1: 
                inline_update_custom_condition_tier()
            with col_2:  
                generate_and_display_test_summary(input_key='cond_tab')

    with custom_test_tier_tab:
        if len(st.session_state.custom_test_tier_list) == 0:
            st.markdown("""<div style="height:400px;"></div>""", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: grey;'>Must create/upload test condition tier (Check instruction on the page 4)</h2>", unsafe_allow_html=True)
        else:
            st.session_state.inline_custom_test_list = st.session_state.custom_test_tier_list
            inline_display_custom_test_tier_df()

            _, col_0, col_1, col_2, _ = st.columns([0.125, 0.25, 0.25, 0.25, 0.125])
            with col_0:
                inline_fetch_custom_test_tier()
            with col_1:
                inline_update_custom_test_tier()
            with col_2:  
                generate_and_display_test_summary(input_key='test_tab')

with display_col:
    long_format_tab, pdf_tab =  st.tabs(['Test Summary - Long Format','Test Summary - pdf',])
   
    if st.session_state.display_test_summary == False:
        if ((len(st.session_state.custom_condition_list) == 0) and 
            (len(st.session_state.custom_test_tier_list) == 0)):
            markdown_msg = "<h2 style='text-align: center; color: grey;'>Please upload your custom condition tier and custom test format tier and click generate the summary table.</h2>"
        elif len(st.session_state.custom_condition_list) == 0:
            markdown_msg = "<h2 style='text-align: center; color: grey;'>Please upload your custom condition tier and click generate the summary table.</h2>"
        elif len(st.session_state.custom_test_tier_list) == 0:
            markdown_msg = "<h2 style='text-align: center; color: grey;'>Please upload your custom test format tier and click generate the summary table.</h2>"
        else:
            markdown_msg = "<h2 style='text-align: center; color: grey;'>Please click the 'Generate the Summary' button to display your test summary table.</h2>"
    
        with long_format_tab:
            st.markdown("""<div style="height:400px;"></div>""", unsafe_allow_html=True)
            st.markdown(markdown_msg, unsafe_allow_html=True)
        with pdf_tab:
            st.markdown("""<div style="height:400px;"></div>""", unsafe_allow_html=True)
            st.markdown(markdown_msg, unsafe_allow_html=True)
    
    else:
        with long_format_tab:
            st.dataframe(
                st.session_state['test_summary_df'],
                use_container_width=True,
                height=data_frame_height,)

        with pdf_tab:
            base64_pdf = generate_base64pdf(generate_pdf_format_df(st.session_state.test_summary_df))

            # Display PDF in Streamlit
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="{data_frame_height}" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
            st.markdown("""<div style="height:30px;"></div>""", unsafe_allow_html=True)
            _, col, _ = st.columns([0.3, 0.4, 0.3], gap='small')
            with col:
                st.download_button(
                    "Download Test Summary",
                    convert_df(st.session_state.test_summary_df),
                    "test_summary.csv",
                    "text/csv",
                    key='download-csv'
                )