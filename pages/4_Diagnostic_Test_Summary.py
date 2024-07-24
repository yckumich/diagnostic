import pandas as pd
from utils.tests_summary_utils.utils import *
from utils.dataframe_utils.utils import convert_selection_to_df
from utils.dataframe_utils.utils_center_tab import get_lab_specific_test_by_laboratory_section
import streamlit as st
import time

#----------------------INIT-----------------------
st.set_page_config(
    page_title="Diagnostic Test Summary",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

if "display_test_summary" not in st.session_state:
    st.session_state.display_test_summary = False

if "test_summary_df" not in st.session_state:
    st.session_state.test_summary_df = None

if "temp_custom_lab_specific_test_by_laboratory_section_df" not in st.session_state:
    st.session_state.temp_custom_lab_specific_test_by_laboratory_section_df = None

if "custom_lab_specific_test_by_laboratory_section_list" not in st.session_state:
    st.session_state.custom_lab_specific_test_by_laboratory_section_list = None


#----------------------MAIN-----------------------
add_sidebar()

build_col, display_col = st.columns([1,1], gap="medium")
temp_lstbl_df_exist = isinstance(st.session_state.temp_custom_lab_specific_test_by_laboratory_section_df, pd.DataFrame)


with build_col:
    if not temp_lstbl_df_exist:
        st.markdown("""<div style="height:400px;"></div>""", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Must create/upload custom test tier and generate Lab Specific - Test By Laboratory table </h2>", unsafe_allow_html=True)
    else:
        if isinstance(st.session_state.custom_lab_specific_test_by_laboratory_section_list, list):
            st.write("### Lab Specific - Test By Laboratory ")
            display_test_by_lab_df(st.session_state.custom_lab_specific_test_by_laboratory_section_list)
            # st.dataframe(st.session_state.custom_lab_specific_test_by_laboratory_section_df, height=700)

            _, col_0, col_1, col_2, _ = st.columns([0.2, 0.2, 0.2, 0.2, 0.2], gap='small')
            with col_0:
                if st.button("Refresh Existing Table"):
                    st.session_state.display_test_summary = False                    
                    df = st.session_state.temp_custom_lab_specific_test_by_laboratory_section_df.copy().dropna(axis=0).reset_index(drop=True)
                    st.session_state.custom_lab_specific_test_by_laboratory_section_list = df.to_dict(orient='records')
                    msg = st.toast("Fetching current custom 'Test By Laboratory' table...")
                    time.sleep(0.7)
                    msg.toast('Fetched ✅')
                    time.sleep(0.7)
                    st.rerun()                    

            with col_1:
                if st.button("Delete Current Table"):
                    st.session_state.custom_lab_specific_test_by_laboratory_section_list = None
                    st.session_state.display_test_summary = False
                    msg = st.toast("Deleting current custom 'Test By Laboratory' table...")
                    time.sleep(0.7)
                    msg.toast('Deleted')
                    time.sleep(0.7)
                    st.rerun()
            with col_2:
                if st.button("Generate Test Summary"):
                    st.session_state.display_test_summary = True
                    st.session_state.test_summary_df = generate_tests_summary(st.session_state.custom_lab_specific_test_by_laboratory_section_list)
                    st.rerun()
        else:
            st.markdown("""<div style="height:420px;"></div>""", unsafe_allow_html=True)
            _, col, _ = st.columns([0.3, 0.4, 0.3], gap='small')
            with col:
                if st.button("Fetch current 'Test By Laboratory' table"):
                    df = st.session_state.temp_custom_lab_specific_test_by_laboratory_section_df.copy().dropna(axis=0).reset_index(drop=True)
                    st.session_state.custom_lab_specific_test_by_laboratory_section_list = df.to_dict(orient='records')
                    msg = st.toast("Fetching current custom 'Test By Laboratory' table...")
                    time.sleep(0.7)
                    msg.toast('Fetched ✅')
                    time.sleep(0.7)
                    st.rerun()

with display_col:
    if not isinstance(st.session_state.custom_lab_specific_test_by_laboratory_section_list, list):
        st.markdown("""<div style="height:400px;"></div>""", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Must fetch Lab Specific - Test By Laboratory table with custom test tier to generate a plot</h2>", unsafe_allow_html=True)

    else:
        if st.session_state.display_test_summary == True:
            st.write("### Test Summary")
            st.dataframe(st.session_state.test_summary_df, height=700)
        else:
            st.markdown("""<div style="height:400px;"></div>""", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: grey;'>Click 'Generate Test Summary' to display Test Summary Table</h2>", unsafe_allow_html=True)
