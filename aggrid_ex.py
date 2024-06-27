import streamlit as st
import pandas as pd
import numpy as np
import random
import string

# Set page configuration
st.set_page_config(page_title="Single Row of Tabs Example", layout="wide")

# Function to generate a random string of given length
def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

# Function to generate random DataFrame with random column names
def generate_random_dataframe(rows, min_cols=3, max_cols=8):
    num_cols = random.randint(min_cols, max_cols)
    col_names = [generate_random_string(random.randint(12, 20)) for _ in range(num_cols)]
    return pd.DataFrame(np.random.rand(rows, num_cols), columns=col_names)

# Function to generate random title
def generate_random_title():
    titles = [
        "Data Overview", "Performance Metrics", "Test Results", "Summary Report",
        "Analysis Data", "Statistical Data", "Experimental Results", "Data Summary",
        "Research Findings", "Data Insights"
    ]
    return random.choice(titles)

# Inject custom CSS
st.markdown(
    """
    <style>
    .stTabs [role="tablist"] {
        display: flex;
        justify-content: space-between;
    }
    .small-title {
        font-size: 18px;
        margin-bottom: 0.5rem;
    }
    .tight-container {
        padding: 0.5rem;
    }
    .stDataFrame {
        margin: 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Single row of tabs with 8 tabs
st.markdown("### Single Row of Tabs")
tabs = st.tabs([
    "Lab-Specific-01", "Test-By-Cond-02", "Cond-By-Test-03", "Another-Tab-04",
    "Specific-05", "By-Cond-Test-06", "By-Test-Cond-07", "Different-Tab-08"
])

# Function to add a random number of dataframes to a tab and display them side by side with titles
def add_dataframes_to_tab():
    num_dataframes = random.randint(1, 3)
    dataframes = [generate_random_dataframe(10) for _ in range(num_dataframes)]
    total_columns = sum(df.shape[1] for df in dataframes)
    
    # Calculate the column width percentage for each DataFrame
    col_widths = [df.shape[1] / total_columns for df in dataframes]
    
    cols = st.columns(num_dataframes)
    for i in range(num_dataframes):
        with cols[i]:
            width_percent = col_widths[i] * 100
            title = generate_random_title()
            st.markdown(f"<div class='small-title'>{title}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='tight-container' style='width: {width_percent}%;'>", unsafe_allow_html=True)
            st.dataframe(dataframes[i])
            st.markdown("</div>", unsafe_allow_html=True)

with tabs[0]:
    add_dataframes_to_tab()

with tabs[1]:
    add_dataframes_to_tab()

with tabs[2]:
    add_dataframes_to_tab()

with tabs[3]:
    add_dataframes_to_tab()

with tabs[4]:
    add_dataframes_to_tab()

with tabs[5]:
    add_dataframes_to_tab()

with tabs[6]:
    add_dataframes_to_tab()

with tabs[7]:
    add_dataframes_to_tab()
