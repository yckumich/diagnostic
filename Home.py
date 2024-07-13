import streamlit as st


st.set_page_config(
    page_title="EDL Tool - Home",
    page_icon="🏠", 
    layout="wide",
    initial_sidebar_state="expanded",
)

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

st.title("Essential Diagnostics Network for Universal Health Coverage")

st.sidebar.success("Select a desired page above.")

st.markdown("""<div style="height:30px;"></div>""", unsafe_allow_html=True)

st.markdown(
    """  
    The **Essential Diagnostics Network project** aims to support Universal Health Coverage (UHC) 
    by developing a rational and effective network of diagnostic services. This initiative is rooted
    in the principles outlined in a comprehensive study focused on optimizing the availability
    and utilization of essential diagnostic tests. The core objectives of the project include 
    enhancing diagnostic capabilities across various levels of healthcare facilities, ensuring 
    equitable access to critical diagnostic tests, and promoting the efficient use of resources 
    to improve patient outcomes.

    #### Key Highlights:
    - **Rational Design:** The project emphasizes a systematic approach to designing diagnostic networks that align with the healthcare needs of different populations.
    It involves identifying essential diagnostic tests that are critical for the effective management of common health conditions.
    
    - **Health Facility Tiers:** The network design considers the capabilities and resources of different tiers of health facilities, from primary to tertiary care.
    The goal is to ensure that each level of care has access to appropriate diagnostic tools, facilitating timely and accurate diagnoses.
    
    - **Condition Levels and Diagnostic Needs:** The project categorizes health conditions based on their severity and diagnostic requirements.
    This categorization helps in prioritizing the allocation of diagnostic resources and tailoring the network to address the most pressing health challenges.
    
    - **Data-Driven Approach:** Leveraging data from various sources, the project aims to create a dynamic and adaptable diagnostic network.
    Continuous monitoring and evaluation are integral to the project, ensuring that the network remains responsive to changing healthcare needs and emerging health threats.
    
    - **Universal Health Coverage:** The ultimate aim of the project is to support UHC by making essential diagnostics accessible and affordable for all.
    By improving diagnostic services, the project contributes to better health outcomes and reduces the burden of disease on communities.
"""
)



st.markdown("""<div style="height:50px;"></div>""", unsafe_allow_html=True)


# Read the paper content
with open("supplements/Rational_Design_Lab_Network.pdf", "rb") as file:
    paper_content = file.read()

# Provide a download button for the paper
st.download_button(
    label="Download the original research paper",
    data=paper_content,
    file_name="research_paper.pdf",
    mime="application/pdf"
)