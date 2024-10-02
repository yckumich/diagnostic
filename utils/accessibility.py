import streamlit as st

def add_skip_link_to_sidebar():
    st.sidebar.markdown("""
        <style>
            /* Hide the skip link by default */
            .skip-link-sidebar {
                position: absolute;
                top: 0;
                left: 0;
                transform: translateY(-100%);
                background: transparent;
                color: blue;
                padding: 8px 16px;
                z-index: 100;
                text-decoration: none;
                opacity: 0;
                transition: transform 0.3s, opacity 0.3s;
            }

            /* Show the skip link when focused (e.g., when pressing Tab) */
            .skip-link-sidebar:focus {
                transform: translateY(0%);
                opacity: 1;
            }

            /* Optional: Adjust the position to be at the top of the sidebar */
            [data-testid="stSidebar"]::before {
                position: absolute;
            }
        </style>
        <a href="#main-content" class="skip-link-sidebar">Skip to main content</a>
        """, unsafe_allow_html=True)

def hide_topmenu():
    # st.markdown('''
    # <style>
    # .stApp [data-testid="stToolbar"]{
    #     display:none;
    # }
    # </style>
    # ''', unsafe_allow_html=True)
    return


# utils/accessibility.py


def set_dataframe_buttons_visibility(show_buttons=True, show_search=True, always_visible=True):
    """
    Modify the visibility and behavior of the download, search, and fullscreen buttons in st.dataframe.

    Parameters:
    - show_buttons (bool): If False, hides the download and fullscreen buttons.
    - show_search (bool): If False, hides the search input field.
    - always_visible (bool): If True, makes the buttons always visible even when the mouse is not hovering.
    """
    css = "<style>"
    
    if not show_buttons:
        css += """
        /* Hide the fullscreen and download buttons */
        button[title="View fullscreen"],
        button[title="Download data as CSV"] {
            display: none;
        }
        """
    
    if not show_search:
        css += """
        /* Hide the search input */
        .stDataFrame [data-baseweb="input"] {
            display: none;
        }
        """
    
    if always_visible:
        css += """
        /* Make the buttons always visible */
        .stDataFrame > div button[title="View fullscreen"],
        .stDataFrame > div button[title="Download data as CSV"],
        .stDataFrame > div div[data-baseweb="input"] {
            visibility: visible !important;
        }
        """
    
    css += "</style>"
    
    st.markdown(css, unsafe_allow_html=True)



def set_dataframe_header_style(background_color="#FFFFFF", font_color="#000000"):
    """
    Modify the header style of st.dataframe components.

    Parameters:
    - background_color (str): The background color for the header (default is white "#FFFFFF").
    - font_color (str): The font color for the header text (default is black "#000000").
    """
    css = f"""
    <style>
    /* Apply styles to the header of st.dataframe */
    .stDataFrame thead tr th {{
        background-color: {background_color} !important;
        color: {font_color} !important;
    }}
    /* Adjust border color if needed */
    .stDataFrame tbody tr td, .stDataFrame thead tr th {{
        border-color: rgba(49, 51, 63, 0.1);
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)