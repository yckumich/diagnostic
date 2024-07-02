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
