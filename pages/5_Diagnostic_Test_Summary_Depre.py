import pandas as pd
from utils.tests_summary_utils.utils import *
from utils.dataframe_utils.utils import convert_selection_to_df
from utils.dataframe_utils.utils_center_tab import get_lab_specific_test_by_laboratory_section
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

if "display_test_summary" not in st.session_state:
    st.session_state.display_test_summary = False

if "test_summary_df" not in st.session_state:
    st.session_state.test_summary_df = None

if "temp_clstbls_df" not in st.session_state:
    st.session_state.temp_clstbls_df = None

if "curr_clstbls_list" not in st.session_state:
    st.session_state.curr_clstbls_list = None


#----------------------MAIN-----------------------
add_sidebar()

build_col, display_col = st.columns([1, 1], gap="medium")
temp_clstbls_df_exist = isinstance(st.session_state.temp_clstbls_df, pd.DataFrame)
curr_clstbls_list_exist = isinstance(st.session_state.curr_clstbls_list, List)

with build_col:
    if not temp_clstbls_df_exist:
        st.markdown("""<div style="height:400px;"></div>""", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Must create/upload custom test tier and generate Lab Specific - Test By Laboratory table (Check instruction on the sidebar)</h2>", unsafe_allow_html=True)
    else:
        if not curr_clstbls_list_exist:
            st.markdown("""<div style="height:420px;"></div>""", unsafe_allow_html=True)
            _, col, _ = st.columns([0.3, 0.4, 0.3], gap='small')
            with col:
                if st.button("Fetch current 'Test By Laboratory' table"):
                    st.session_state.curr_clstbls_list = st.session_state.temp_clstbls_df.copy().dropna(axis=0).reset_index(drop=True).to_dict(orient='records')
                    msg = st.toast("Fetching current custom 'Test By Laboratory' table...")
                    time.sleep(0.7)
                    msg.toast('Fetched ✅')
                    time.sleep(0.7)
                    st.rerun()
        else:
            st.write("### Lab Specific - Test By Laboratory ")
            display_test_by_lab_df(st.session_state.curr_clstbls_list)

            _, col_0, col_1, col_2, _ = st.columns([0.2, 0.2, 0.2, 0.2, 0.2], gap='small')

            with col_0:
                if st.button("Refresh Current Table"):
                    st.session_state.display_test_summary = False                    
                    st.session_state.curr_clstbls_list = st.session_state.temp_clstbls_df.copy().dropna(axis=0).reset_index(drop=True).to_dict(orient='records')
                    msg = st.toast("Fetching current 'Test By Laboratory' table...")
                    time.sleep(0.7)
                    msg.toast('Refreshed ✅')
                    time.sleep(0.7)
                    st.rerun()                    

            with col_1:
                if st.button("Delete Current Table"):
                    st.session_state.curr_clstbls_list = None
                    st.session_state.temp_clstbls_df = None
                    st.session_state.display_test_summary = False
                    msg = st.toast("Deleting current custom 'Test By Laboratory' table...")
                    time.sleep(0.7)
                    msg.toast('Deleted 🗑️')
                    time.sleep(0.7)
                    st.rerun()

            with col_2:
                if st.button("Generate Test Summary"):
                    st.session_state.display_test_summary = True
                    st.session_state.test_summary_df = generate_tests_summary(pd.DataFrame.from_dict(st.session_state.curr_clstbls_list))
                    st.rerun()

with display_col:
    if not isinstance(st.session_state.curr_clstbls_list, List):
        st.markdown("""<div style="height:400px;"></div>""", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Must fetch Lab Specific - Test By Laboratory table with custom test tier to generate the summary table</h2>", unsafe_allow_html=True)

    else:
        if st.session_state.display_test_summary == True:
            st.write("### Test Summary")
            # generate base64 PDF
            base64_pdf = generate_base64pdf(st.session_state.test_summary_df)

            # Display PDF in Streamlit
            pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
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
                            
        else:
            st.markdown("""<div style="height:400px;"></div>""", unsafe_allow_html=True)
            st.markdown("<h2 style='text-align: center; color: grey;'>Click 'Generate Test Summary' to display Test Summary Table</h2>", unsafe_allow_html=True)
