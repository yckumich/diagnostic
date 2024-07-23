import pandas as pd
from utils.tests_summary_utils.utils import *
import streamlit as st

#----------------------INIT-----------------------
st.set_page_config(
    page_title="Diagnostic Test Summary",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)
if "temp_custom_lab_specific_test_by_laboratory_section_df" not in st.session_state:
    st.session_state.temp_custom_lab_specific_test_by_laboratory_section_df = None

if "custom_lab_specific_test_by_laboratory_section_df" not in st.session_state:
    st.session_state.custom_lab_specific_test_by_laboratory_section_df = None
#----------------------MAIN-----------------------
add_sidebar()
build_col, display_col = st.columns([1,1], gap="small")

with build_col:
    ...

with display_col:
    if not isinstance(st.session_state.custom_lab_specific_test_by_laboratory_section_df, pd.DataFrame):
        st.markdown("""<div style="height:400px;"></div>""", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Must build/upload Custom Lab Specific Test By Laboratory Section dataframe to render the plot</h2>", unsafe_allow_html=True)

