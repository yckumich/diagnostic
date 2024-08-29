import pandas as pd
import streamlit as st

#----------------------INIT-----------------------
st.set_page_config(
    page_title="Custom Test Format Tier",
    layout="wide",
    initial_sidebar_state="expanded"
)

from utils.test_tier_utils.utils import *

UM_Block_Logo = "static/Block_M-Hex.png"
UM_Extended_Logo = "static/U-M_Logo-Horizontal-Hex.png"

st.logo(UM_Extended_Logo, icon_image=UM_Block_Logo)

#----------------------MAIN-----------------------
initialize_session_state()
add_sidebar()
build_col, display_col = st.columns([1,1], gap="small")
    
with build_col:
    st.write("### Custom Test-Format Tier Table")
    display_custom_test_tier_df()

    _, col_1, col_2, col_3, _ = st.columns([0.125, 0.25, 0.25, 0.25, 0.125])
    with col_1:
        delete_current_custom_test_tier_df()
    with col_2:
        save_current_coustom_test_tier_df()
    with col_3:
        load_lancet_test_format_tier_df()

    # Form to add a new condition
    add_new_condition_tier_form()
    upload_custom_tier_tier_csv()

with display_col:
    if len(st.session_state[CUSTOM_TEST_TIER_LIST_KEY]) > 0:
        if not st.session_state[SHOW_TEST_TIER_PLOT_KEY]:
            st.markdown("""<div style="height:500px;"></div>""", unsafe_allow_html=True)
            _, col, _ = st.columns([0.35, 0.3, 0.35])
            with col:
                if st.button('Render Custom Test-Format Tier Plot'):
                    st.session_state[SHOW_TEST_TIER_PLOT_KEY] = True
                    st.rerun()
        else:
            render_custom_test_format_tier_plot_section()
    else:
        st.markdown("""<div style="height:400px;"></div>""", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; color: grey;'>Must build/upload custom test tier dataframe to render the plot</h2>", unsafe_allow_html=True)

