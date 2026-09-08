import streamlit as st

from style import get_sidebar_style

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.logo(image="static/CGHE_formal_horizontal.png",
        icon_image="static/CGHE_formal_horizontal.png",
        size="large")

get_sidebar_style()

st.title("About This Website")

st.markdown("""<div style="height:20px;"></div>""", unsafe_allow_html=True)

st.markdown(
    """
    This website provides two complementary decision-support tools for exploring essential
    diagnostics and planning their placement across tiers of a health system:
    - The **Essential Diagnostics Explorer** links diseases, medicines, in vitro diagnostics, and radiological examinations.
    - The **Diagnostic Network Planner** helps users examine how diagnostic services could be distributed across different tiers of care.

    #### Support and Contributions
    - The **University of Michigan CGHE** funded the development of the web-based decision-support tools,
    created the software and code that power them, and hosts this website.

    - The **World Health Organization (WHO)** funded the expansion of the disease-medicine-diagnostic
    database described in *Essential Diagnostics for the Use of World Health Organization Essential
    Medicines*, published in Clinical Chemistry.

    - The **Lancet Commission on Diagnostics** supported further development of the evidence base and the
    diagnostic-network planning model. The Commission was funded by the **Bill & Melinda Gates
    Foundation** under grant **OPP1204832**.

    - We gratefully acknowledge these organizations, as well as the researchers, clinicians, laboratory
    professionals, policymakers, and technical contributors whose work made these resources possible.

    - The content and conclusions presented through these tools are those of the project contributors
    and do not necessarily represent the official positions of the World Health Organization, the
    Bill & Melinda Gates Foundation, the Lancet Commission on Diagnostics, or other supporting
    organizations.

    #### Contact
    Questions and suggestions may be sent to
    [leeschro@med.umich.edu](mailto:leeschro@med.umich.edu), including:
    - Questions about using the tools
    - Requests to add, revise, or correct tool content
    - Suggestions for expanding the diseases included in the Diagnostic Network Planner
    - Other feedback about the database or decision-support tools
"""
)
