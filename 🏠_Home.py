import streamlit as st

from style import get_sidebar_style

st.set_page_config(
    page_title="Essential Diagnostics for Universal Health Coverage",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.logo(image="static/CGHE_formal_horizontal.png",
        icon_image="static/CGHE_formal_horizontal.png",
        size="large")

get_sidebar_style()
        

##INITIALIZE SESSION STATE
if "custom_condition_list" not in st.session_state:
    st.session_state.custom_condition_list = []

if "custom_condition_df" not in st.session_state:
    st.session_state.custom_condition_df = None

if 'show_plot' not in st.session_state:
    st.session_state['show_plot'] = False

if "custom_test_tier_list" not in st.session_state:
    st.session_state.custom_test_tier_list = []

if "custom_test_tier_df" not in st.session_state:
    st.session_state.custom_test_tier_df = None

if 'show_test_tier_plot' not in st.session_state:
    st.session_state['show_test_tier_plot'] = False


st.title("Essential Diagnostics for Universal Health Coverage")

st.markdown("""<div style="height:20px;"></div>""", unsafe_allow_html=True)

st.markdown(
    """
    Access to appropriate diagnostic services is essential for effective treatment and universal
    health coverage. This website provides decision-support tools to help policymakers, health
    system planners, researchers, and other stakeholders identify essential diagnostics and design
    integrated, tiered diagnostic networks.

    **There are two tools built into this decision support:**
    - **Essential Diagnostics Explorer:** Explore which diagnostics are needed for particular diseases and medicines, and which diseases and medicines are supported by particular diagnostics
    - **Diagnostic Network Planner:** Where diagnostics should be placed within a tiered health system

    #### Essential Diagnostics Explorer: Explore diseases, medicines, and diagnostics
    Use the relational database to explore connections among:
    - Diseases and clinical conditions
    - Essential medicines
    - In vitro diagnostics & radiological examinations

    Comprehensive filters allow you to focus on selected diseases, medicines, or diagnostics. Use the results to:
    - Identify diagnostics needed to manage specific diseases
    - Determine which diagnostics support the safe and effective use of essential medicines
    - Explore the clinical applications of selected diagnostics
    - Inform essential diagnostics lists, policies, and planning

    #### Diagnostic Network Planner: Design a tiered diagnostic network
    Use the Lancet Commission on Diagnostics model to explore where diagnostic services could be
    placed across different tiers of a country or health system. The tool currently supports 20 high
    burden diseases. The model includes diseases projected to cause a substantial burden in low- and
    middle-income countries in 2030 and 2040.

    The tool allows you to:
    - Assign diseases and levels of disease severity to different tiers of care
    - Specify which diagnostic formats could potentially be supported at each tier in a system
    - Adapt the model to the organization and capabilities of a particular health system
    - Support the development of national essential diagnostics lists and diagnostic-network strategies
"""
)

st.page_link("pages/5_📖_Background.py",
             label="Learn more about the project in Background",
             icon="📖")



# Display the WHO video. st.video takes no width, so the surrounding columns are
# what centre it and set its size. Streamlit also hands the YouTube embed a 4:3
# box, which letterboxes a 16:9 video, so the ratio is forced here.
VIDEO_URL = "https://youtu.be/OgLqIgqLkqg?si=1cKn3HypBFMRPcR9"

st.markdown(
    """
    <style>
    [data-testid="stVideo"] {
        aspect-ratio: 16 / 9;
        height: auto !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

_, video_col, _ = st.columns([0.2, 0.6, 0.2])
with video_col:
    st.video(VIDEO_URL)