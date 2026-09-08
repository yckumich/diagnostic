import streamlit as st

from style import get_sidebar_style

st.set_page_config(
    page_title="Background",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.logo(image="static/CGHE_formal_horizontal.png",
        icon_image="static/CGHE_formal_horizontal.png",
        size="large")

get_sidebar_style()

st.title("Background")

st.markdown("""<div style="height:20px;"></div>""", unsafe_allow_html=True)

st.markdown(
    """
    ## Essential Diagnostics for Universal Health Coverage
    Diagnostic services are fundamental to effective health care. Without access to appropriate
    testing, diseases may go undetected, medicines may be used ineffectively or unsafely, and health
    systems may struggle to allocate limited resources.

    This website supports efforts to improve access to essential diagnostics by providing tools that
    connect diseases, medicines, and diagnostics and help users plan diagnostic services across
    different tiers of a health system.

    #### WHO Essential Diagnostics List
    The World Health Organization established the
    [WHO Model List of Essential In Vitro Diagnostics](https://www.who.int/teams/health-product-policy-and-standards/assistive-and-medical-technology/medical-devices/selection-access-and-use-in-vitro),
    commonly known as the Essential Diagnostics List or EDL, in 2018. It was created to complement
    the WHO Model List of Essential Medicines, first published in 1977.

    The EDL reflects the understanding that access to essential medicines alone is not sufficient.
    Appropriate in vitro diagnostics (clinical laboratory tests performed on specimens such as blood,
    urine, or tissue) are often necessary to identify diseases, select treatments, monitor treatment
    effectiveness, and promote the safe use of medicines.

    Diagnostics are therefore a fundamental component of universal health coverage.

    The WHO EDL is maintained with guidance from the
    [Strategic Advisory Group of Experts on In-Vitro Diagnostics](https://www.who.int/groups/who-strategic-advisory-group-of-experts-on-in-vitro-diagnostics).
    The fifth edition can be accessed digitally through the WHO electronic Essential Diagnostics List
    ([WHO eEDL](https://edl.who-healthtechnologies.org/)).

    #### National Essential Diagnostics Lists
    The [Lancet Commission on Diagnostics](https://www.thelancet.com/commissions-do/diagnostics)
    recommended that countries adopt:

    > A national diagnostics strategy, based on an integrated and tiered network, including an
    > evidence-based essential diagnostics list, with a prioritised subset for universal health
    > coverage.

    In 2023, the 76th World Health Assembly adopted a resolution on
    [Strengthening Diagnostics Capacity](https://www.who.int/activities/strengthening-diagnostics-capacity).
    The resolution encouraged countries to consider developing national essential diagnostics lists
    by adapting the WHO Model List of Essential In Vitro Diagnostics and WHO priority medical-device
    lists to their local contexts.

    The Essential Diagnostics initiative emphasizes that diagnostic planning must address both:
    - The tests that are essential for meeting population health needs
    - The locations and tiers of care at which those tests should be available

    #### Development of the relational database underlying the Essential Diagnostics Explorer tool
    The relational database on this website links diseases, medicines, and diagnostics. Its
    foundations were described in two publications:
    - *[Time for a Model List of Essential Diagnostics](https://pubmed.ncbi.nlm.nih.gov/27355530/)* — New England Journal of Medicine, 2016
    - *[Essential Diagnostics for the Use of World Health Organization Essential Medicines](https://pubmed.ncbi.nlm.nih.gov/29871869/)* — Clinical Chemistry, 2018

    The database was subsequently expanded through the Lancet Commission on Diagnostics, including
    recognition of the role of radiological examinations in essential diagnostic services.

    The current decision-support tool includes relationships among:
    - Diseases and clinical conditions
    - Essential medicines
    - In vitro diagnostics & radiological examinations

    Users can filter the database to examine specific diseases, medicines, or diagnostics. This can
    reveal which diagnostics support the management of a particular disease, which tests are
    associated with the use of a medicine, or how a diagnostic applies across multiple conditions.

    #### Development of the Diagnostic Network Planner tool
    The Lancet Commission on Diagnostics also developed a model to support the rational design of
    tiered laboratory and diagnostic systems. It is based on the premise that a diagnostic should
    generally be available at the tier for which the patient needing the diagnostic is being treated.
    Or, in the case of laboratory testing, that there is a robust specimen transport system at the
    tier that can ensure timely results.

    Essential medicines lists are commonly adapted at the country level, with medicines assigned to
    different tiers of the health system. Diagnostic planning requires a similar approach. Although
    the WHO EDL distinguishes between tests that can be used in settings with and without
    laboratories, national planning often requires more detailed decisions about where particular
    diagnostic services should be placed.

    The model allows users to:
    - Adapt assumptions to reflect a country's health-system structure and resources
    - Assign diseases and levels of disease severity to different tiers of care
    - Change the tiers at which diseases are managed
    - Specify the diagnostic formats that could potentially be logistically supported at each tier, if necessary
    - Examine the resulting distribution of recommended diagnostic services

    The model currently includes diagnostics and medicines associated with 20 diseases projected to
    cause a substantial burden in low- and middle-income countries in 2030 and 2040.

    The model and its methods are described in:
    - *[Rational Design of an Essential Diagnostics Network to Support Universal Health Coverage: A Modeling Analysis](https://pubmed.ncbi.nlm.nih.gov/36183079/)* — BMC Medicine, 2022

    #### Purpose of the tools
    The website's decision-support tools serve two complementary functions.

    **1. Essential Diagnostics Explorer: Identify diagnostic needs**

    The relational database helps users examine the connections among diseases, medicines, and
    diagnostics. It can support the development or review of essential diagnostics lists and help
    policymakers focus on selected health priorities.

    **2. Diagnostic Network Planner: Plan where diagnostic services should be available**

    The tiered-network model helps users explore the placement of diagnostic services across a health
    system. It is particularly relevant to the development of national essential diagnostics lists,
    laboratory strategies, and integrated diagnostic networks.

    The tools are intended to support evidence-informed decision-making. Their results should be
    interpreted in light of local disease burden, clinical guidelines, infrastructure, workforce
    capacity, supply chains, financing, and other country-specific considerations.

    #### Publications and resources
"""
)

# title, source, button label, url
RESOURCES = [
    ("Time for a Model List of Essential Diagnostics",
     "New England Journal of Medicine, 2016",
     "View publication",
     "https://pubmed.ncbi.nlm.nih.gov/27355530/"),
    ("Essential Diagnostics for the Use of World Health Organization Essential Medicines",
     "Clinical Chemistry, 2018",
     "View publication",
     "https://pubmed.ncbi.nlm.nih.gov/29871869/"),
    ("Rational Design of an Essential Diagnostics Network to Support Universal Health Coverage: "
     "A Modeling Analysis",
     "BMC Medicine, 2022",
     "View publication",
     "https://pubmed.ncbi.nlm.nih.gov/36183079/"),
    ("The Lancet Commission on Diagnostics",
     "",
     "View report",
     "https://www.thelancet.com/commissions-do/diagnostics"),
    ("WHO Model List of Essential In Vitro Diagnostics 4th edition",
     "",
     "View WHO resources",
     "https://www.who.int/publications/i/item/9789240081093"),
    ("WHO electronic Essential Diagnostics List",
     "",
     "Access the WHO eEDL",
     "https://edl.who-healthtechnologies.org/"),
]

for title, source, button_label, url in RESOURCES:
    text_col, button_col = st.columns([0.7, 0.3], gap="small")
    with text_col:
        st.markdown(f"**{title}**  \n{source}" if source else f"**{title}**")
    with button_col:
        st.link_button(button_label, url, use_container_width=True)
    st.markdown("""<div style="height:8px;"></div>""", unsafe_allow_html=True)
