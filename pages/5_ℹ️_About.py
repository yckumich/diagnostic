import streamlit as st

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.logo(image="static/CGHE_formal_horizontal.png",
        icon_image="static/CGHE_formal_horizontal.png",
        size="large")

st.title("About")

st.info(
    "This section is under construction. "
    "Content describing the project background, methodology, data sources, "
    "team, and contact information will be added here.",
    icon="🚧"
)
