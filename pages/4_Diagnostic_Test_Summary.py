#----------------------INIT-----------------------
import streamlit as st
st.set_page_config(
    page_title="Diagnostic Test Summary",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)
UM_Block_Logo = "static/Block_M-Hex.png"
UM_Extended_Logo = "static/U-M_Logo-Horizontal-Hex.png"

st.logo(UM_Extended_Logo, icon_image=UM_Block_Logo)

from utils.tests_summary_utils.utils import *
from style import get_style_markdown
from utils.accessibility import *

def initialize_session_state():
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
initialize_session_state()
hide_topmenu()
add_skip_link_to_sidebar()
add_sidebar()
get_style_markdown()

st.write("### Test Summary")
build_col, display_col = st.columns([1, 1], gap="medium")

with build_col:
    st.markdown('<div id="main-content"></div>', unsafe_allow_html=True)

    custom_cond_tier_tab, custom_test_tier_tab  = st.tabs(['Custom Condition Tier', 'Custom Test-Format Tier', ])

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
    st.markdown("""<div style="height:10px;"></div>""", unsafe_allow_html=True)
    long_format_tab, pdf_tab =  st.tabs(['Test Summary - Long Format','Test Summary - pdf',])
   
    if st.session_state.display_test_summary == False:
        display_placeholder_message(long_format_tab, pdf_tab)

    else:
        with long_format_tab:
            st.dataframe(
                st.session_state['test_summary_df'],
                use_container_width=True,
                height=DATA_FRAME_HEIGHT,)

        with pdf_tab:
            display_pdf_summary()