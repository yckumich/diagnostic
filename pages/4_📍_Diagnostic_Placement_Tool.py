#----------------------INIT-----------------------
import streamlit as st
st.set_page_config(
    page_title="Diagnostic Placement Tool",
    page_icon="📍",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.logo(image="static/CGHE_formal_horizontal.png",
        icon_image="static/CGHE_formal_horizontal.png",
        size="large")

import streamlit as st
from style import get_style_markdown
from utils.tests_summary_utils import utils as U

st.session_state.setdefault("display_test_summary", False)
st.session_state.setdefault("test_summary_df", None)
st.session_state.setdefault("custom_condition_list", [])
st.session_state.setdefault("custom_test_tier_list", [])

if (not st.session_state.custom_condition_list or
    not st.session_state.custom_test_tier_list):
    U._reset_test_summary() 


#----------------------MAIN-----------------------
# initialize_session_state()
U.add_sidebar()
get_style_markdown()

st.write("### Diagnostic Placement Tool")
left, right = st.columns([1, 1], gap="medium")

with left:
    cond_tab, test_tab = st.tabs(["Custom Condition Tier", "Custom Test-Format Tier"])

    # ---- Condition Tier Tab ----
    with cond_tab:
        if not st.session_state.custom_condition_list:
            st.info("Create or upload a **Custom Condition Tier**.")
        else:
            U.condition_editor()  # live editor
            st.divider()
            U.generate_and_display_test_summary("cond_tab")

    # ---- Test-Format Tier Tab ----
    with test_tab:
        if not st.session_state.custom_test_tier_list:
            st.info("Create or upload a **Custom Test-Format Tier**.")
        else:
            U.test_tier_editor()
            st.divider()
            U.generate_and_display_test_summary("test_tab")

with right:
    long_tab, pdf_tab = st.tabs(
        ["Test Summary - Long Format", "Test Summary - PDF"]
    )

    if not st.session_state.display_test_summary:
        U.display_placeholder_message(long_tab, pdf_tab)
    else:
        with long_tab:
            st.dataframe(
                st.session_state.test_summary_df,
                use_container_width=True,
                height=U.DATA_FRAME_HEIGHT,
            )
        with pdf_tab:
            U.display_pdf_summary()

