import streamlit as st

def get_style_markdown():

    return st.markdown(
        """
        <style>
        .stTabs [role="tablist"] {
            display: flex;
            justify-content: space-between;
        }
        .small-title {
            font-size: 14px;
            margin-top: 2rem;
            margin-bottom: 0rem;
        }
        .tight-container {
            padding: 0.5rem;
        }
        .stDataFrame {
            margin: 0;
        }
        [data-testid="stExpander"] details:hover summary {
            background-color: rgba(119, 244, 121, 0.1);
            color: darkgreen;
        }
        </style>
        """,
        unsafe_allow_html=True
        )


def get_sidebar_style():
    """Group the page nav into sections, per Lee's SideBar spec.

    Streamlit builds the nav from the pages/ filenames and has no hook for section
    headings, so each heading is injected as a ::before on the nav item that starts
    its group.

    Headings are anchored to the page URL rather than nth-child, so adding or
    reordering pages can only drop a heading, never silently move one onto the wrong
    item. "Project Information" sits on Background, falling back to About while the
    Background page does not exist yet (WI-4); it relocates on its own once it does.

    Depends on Streamlit 1.39.0's stSidebarNavItems DOM (ul > li > div > a) - re-check
    if that pin moves.
    """
    return st.markdown(
        """
        <style>
        /* Streamlit clips nav labels (nowrap + ellipsis); let the long ones wrap
           instead so no page name is cut off. */
        [data-testid="stSidebarNavItems"] a[data-testid="stSidebarNavLink"] {
            align-items: flex-start;
        }
        [data-testid="stSidebarNavItems"] a[data-testid="stSidebarNavLink"] > span:last-child {
            white-space: normal;
            overflow: visible;
            text-overflow: clip;
        }
        /* The icon box is only as tall as the emoji, so aligning it flush to the top
           leaves it riding above the text. Give it the height of one line and centre
           the glyph in it, so it lines up with the label's first line. */
        [data-testid="stSidebarNavItems"] a[data-testid="stSidebarNavLink"] > span:first-child:not(:last-child) {
            height: 2rem;
            align-items: center;
        }

        [data-testid="stSidebarNavItems"] > li:has(a[href*="/Explore_Diseases_Medicines_and_Diagnostics"])::before,
        [data-testid="stSidebarNavItems"] > li:has(a[href*="/Step_1_-_Set_Condition_Tiers"])::before,
        [data-testid="stSidebarNavItems"] > li:has(a[href*="/Background"])::before,
        [data-testid="stSidebarNavItems"]:not(:has(a[href*="/Background"])) > li:has(a[href*="/About"])::before {
            display: block;
            margin: 1rem 1.5rem 0.25rem 1.5rem;
            padding: 0.75rem 0.5rem 0 0.5rem;
            border-top: 1px solid rgba(128, 128, 128, 0.35);
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            color: inherit;
            opacity: 0.65;
        }
        [data-testid="stSidebarNavItems"] > li:has(a[href*="/Explore_Diseases_Medicines_and_Diagnostics"])::before {
            content: "Essential Diagnostics Explorer";
        }
        [data-testid="stSidebarNavItems"] > li:has(a[href*="/Step_1_-_Set_Condition_Tiers"])::before {
            content: "Diagnostic Network Planner";
        }
        [data-testid="stSidebarNavItems"] > li:has(a[href*="/Background"])::before,
        [data-testid="stSidebarNavItems"]:not(:has(a[href*="/Background"])) > li:has(a[href*="/About"])::before {
            content: "Project Information";
        }
        </style>
        """,
        unsafe_allow_html=True
        )
