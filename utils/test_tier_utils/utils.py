import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st
from data.database import get_view_df
import time


CUSTOM_TEST_TIER_LIST_KEY = "custom_test_tier_list"
CUSTOM_TEST_TIER_DF_KEY = "custom_test_tier_df"
SHOW_TEST_TIER_PLOT_KEY = 'show_test_tier_plot'
TEST_FORMAT = 'test_format'
CUSTOM_TEST_TIER = 'custom_test_tier'

def retrieve_gbd_test_formats():
    """
    Retrieves a sorted list of unique test formats associated with conditions marked as 'lancet_gbd' in the 'conditions' CSV file.

    This function performs the following steps:
    1. Loads the view data from the database using the `get_view_df` function.
    2. Reads the 'conditions.csv' file to identify conditions marked as 'lancet_gbd'.
    3. Filters the test formats in the view data that are associated with the identified conditions.
    4. Returns a sorted list of unique test formats.

    Returns:
    List[str]: A sorted list of unique test formats associated with 'lancet_gbd' conditions.
    """

    view_df = get_view_df()
    condition_names_list = sorted(pd.read_csv("static/conditions.csv").query("lancet_gbd == 'Yes'")['condition_name'].to_list(), key=str.casefold)
    test_format_list = set(view_df[view_df['conditionname'].isin(condition_names_list)][TEST_FORMAT].dropna())
    del view_df
    return sorted(test_format_list, key=str.casefold)

GDB_TEST_FORMAT_LIST = retrieve_gbd_test_formats()


def initialize_session_state():

    if CUSTOM_TEST_TIER_LIST_KEY not in st.session_state:
        st.session_state[CUSTOM_TEST_TIER_LIST_KEY] = []

    if CUSTOM_TEST_TIER_DF_KEY not in st.session_state:
        st.session_state[CUSTOM_TEST_TIER_DF_KEY] = None

    if SHOW_TEST_TIER_PLOT_KEY not in st.session_state:
        st.session_state[SHOW_TEST_TIER_PLOT_KEY] = False


def add_new_condition_tier_form():
    """
    Displays a form in the Streamlit app to add a new test format instance to the custom test tier list.

    This function does the following:
    1. Writes a header for the form.
    2. Creates a form in Streamlit for adding a new test format instance.
    3. Adds a select box for choosing a test format from the global list `GDB_TEST_FORMAT_LIST`.
    4. Adds a select box for choosing the test format tier (Primary, Secondary, Tertiary).
    5. Adds a submit button that, when clicked, calls the `add_new_test_tier` function and clears the form upon submission.
    """
    st.write("### Add a New Test Format Instance")
    with st.form("new_test_tier", clear_on_submit=True):
        st.selectbox("Test Format", GDB_TEST_FORMAT_LIST, key=TEST_FORMAT)
        st.selectbox("Test-Format Tier", ["Primary", "Secondary", "Tertiary"], key=CUSTOM_TEST_TIER)
        st.form_submit_button("Add", on_click=add_new_test_tier)


def display_upload_warning():
    st.warning(
        body="Columns 'test_format' and 'custom_test_tier' must be present in the uploaded CSV file",
        icon="⚠️"
    )


def upload_custom_tier_tier_csv():
    """
    Displays a section in the Streamlit app for uploading a custom test-format tier CSV file.

    This function does the following:
    1. Writes a header for the CSV upload section.
    2. Provides a file uploader widget to upload a CSV file.
    3. If a file is uploaded and the 'Upload' button is clicked, it calls the function
       `handle_custom_test_format_csv_upload` to process the uploaded file.
    """
    st.write("### Upload a Custom Test-Format Tier CSV")
    test_tier_csv = st.file_uploader("upload a CSV file", type={"csv", "txt"})
    if (test_tier_csv is not None) and (st.button("Upload")):
        handle_custom_test_format_csv_upload(test_tier_csv)


def handle_custom_test_format_csv_upload(test_tier_csv):
    """
    Handles the processing of the uploaded custom test-format tier CSV file.

    This function does the following:
    1. Reads the uploaded CSV file into a DataFrame.
    2. Checks if the DataFrame contains the required columns 'test_format' and 'custom_test_tier'.
    3. If the required columns are present, updates the session state with the new data.
    4. If the required columns are not present, displays a warning message.
    5. Handles any exceptions that occur during the file upload process and displays an error message.

    Parameters:
    test_tier_csv (UploadedFile): The uploaded CSV file containing the custom test-format tiers.
    """
    try:
        uploaded_df = pd.read_csv(test_tier_csv)
        uploaded_df_cols = list(uploaded_df.columns)
        essential_cols =  [TEST_FORMAT,CUSTOM_TEST_TIER,]
        if (len(uploaded_df_cols) != 2) or len(set(uploaded_df_cols).intersection(set(essential_cols))) != 2:
            display_upload_warning()

        else:
            st.session_state[CUSTOM_TEST_TIER_LIST_KEY] = uploaded_df.to_dict(orient='records')
            st.session_state[SHOW_TEST_TIER_PLOT_KEY] = False
            st.rerun()
    except Exception as e:
        st.error(f"An error occurred while uploading the file: {e}")


def render_custom_test_format_tier_plot_section():
    fig = create_test_tier_plot(pd.DataFrame(st.session_state[CUSTOM_TEST_TIER_LIST_KEY]))
    st.pyplot(fig)

    st.markdown("""<div style="height:50px;"></div>""", unsafe_allow_html=True)
    _, col1, col2, col3, _ = st.columns([0.23, 0.17, 0.17, 0.2, 0.23], gap='small')
    with col1:
        if st.button('Redraw Plot'):
            st.rerun()
    with col2:
        if st.button('Delete Plot'):
            st.session_state[SHOW_TEST_TIER_PLOT_KEY] = False
            st.rerun()        
    with col3:
        st.download_button(
            label="Download Table",
            data=pd.DataFrame(st.session_state[CUSTOM_TEST_TIER_LIST_KEY]).to_csv(index=False),
            file_name='custom_test_tier.csv',
            mime='text/csv',
        )


@st.cache_data(ttl=3600)
def create_test_tier_plot(df):
    """
    Creates and returns a test-format tier plot based on the given DataFrame.
    
    Parameters:
    df (DataFrame): DataFrame containing 'test_format' and 'custom_test_tier' columns.
    
    Returns:
    Figure: A matplotlib figure object representing the test-format tiers by health facility tier.
    """

    # Define the color for applicable tiers
    applicable_color = "skyblue"
    not_applicable_color = "white"

    # Define the tiers and their ordinal relationship
    tiers = ["Primary", "Secondary", "Tertiary"]
    tier_indices = {tier: idx for idx, tier in enumerate(tiers)}

    # Create a column to sort the DataFrame
    df['tier_index'] = df[CUSTOM_TEST_TIER].map(tier_indices)
    df = df.sort_values(by=['tier_index', TEST_FORMAT], key=lambda col: col.str.casefold() if col.name == TEST_FORMAT else col).reset_index(drop=True)

    # Extract the sorted test names
    tests = df[TEST_FORMAT].unique()

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, int(df[TEST_FORMAT].nunique()/3.5)))

    # Draw the grid and rectangles
    for i, test in enumerate(tests):
        # Determine the highest applicable tier for the current test
        highest_tier = None
        for tier in tiers:
            if not df[(df[TEST_FORMAT] == test) & (df[CUSTOM_TEST_TIER] == tier)].empty:
                highest_tier = tier

        for j, tier in enumerate(tiers):
            if highest_tier and tier_indices[tier] >= tier_indices[highest_tier]:
                # Highlight this cell if it's the designated tier or above
                rect = patches.Rectangle(
                    (j, i), 1, 1,
                    linewidth=1, edgecolor='black', facecolor=applicable_color
                )
            else:
                # Add an empty rectangle for "not applicable" cases
                rect = patches.Rectangle(
                    (j, i), 1, 1,
                    linewidth=1, edgecolor='black', facecolor=not_applicable_color
                )
            ax.add_patch(rect)

    # Set the axis limits and labels
    ax.set_xlim(0, len(tiers))
    ax.set_ylim(0, len(tests))
    ax.set_xticks([0.5, 1.5, 2.5])
    ax.set_xticklabels(tiers)
    ax.set_xlabel("Health Facility Tier")
    ax.set_title("Test-Format by Health Facility Tier")

    # Adjust y-tick positions to the center of each row
    ytick_positions = [i + 0.5 for i in range(len(tests))]
    ax.set_yticks(ytick_positions)
    ax.set_yticklabels(tests)
    ax.set_ylabel("Test-Format Name")

    legend_elements = [
        patches.Patch(facecolor=applicable_color, edgecolor='black', label='Applicable'),
        patches.Patch(facecolor=not_applicable_color, edgecolor='black', label='Not applicable')
    ]
    ax.legend(handles=legend_elements, title="Test Format Tier", loc='center left', bbox_to_anchor=(1, 0.5))

    # Show the plot
    plt.gca().invert_yaxis()
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    return fig


def add_new_test_tier():
    """
    Adds a new test tier record to the custom test tier list stored in the session state.
    The new record is added based on the current values of 'test_format' and 'custom_test_tier' in the session state.
    """
    st.session_state.custom_test_tier_list.append(
        {
            TEST_FORMAT: st.session_state.test_format,
            CUSTOM_TEST_TIER: st.session_state.custom_test_tier,
        }
    )


def test_tier_delete_callback():
    """
    Callback function to delete rows from the custom test tier list based on user interaction.
    If the 'delete' checkbox is checked for a row, that row is removed from the custom test tier list.
    Otherwise, updates the values in the custom test tier list based on user edits.
    """

    edited_rows = st.session_state["test_tier_data_editor"]["edited_rows"]
    for idx, value in edited_rows.items():
        if ('delete' in value.keys()) and (value["delete"] is True):
            st.session_state["custom_test_tier_list"].pop(idx)
        else:
            for k,v in value.items():
                st.session_state["custom_test_tier_list"][idx][k] = v


def display_custom_test_tier_df():
    """
    Displays the custom test tier list as a data editor in Streamlit.
    Allows users to view and mark rows for deletion. The 'delete' column is added
    to allow users to mark rows for deletion.
    """

    custom_test_tier_df = pd.DataFrame(st.session_state["custom_test_tier_list"])
    column_config = {
        TEST_FORMAT: st.column_config.Column(
            disabled=True,
            help='Test Format'
        ),
        CUSTOM_TEST_TIER: st.column_config.SelectboxColumn(
            help='Custom Test Tier',
            options=['Primary','Secondary','Tertiary'],
            required=True,
        )
    }
    custom_test_tier_df["delete"] = False

    # Make Delete be the first column
    custom_test_tier_df = custom_test_tier_df[
        ["delete"] + custom_test_tier_df.columns[:-1].tolist()
    ]

    st.data_editor(
        custom_test_tier_df,
        key="test_tier_data_editor",
        on_change=test_tier_delete_callback,
        hide_index=False,
        column_config=column_config,
        use_container_width=True
    )


def delete_current_custom_test_tier_df():
    """
    Deletes the current custom test tier table from the session state.
    Resets the 'custom_test_tier_list', 'show_test_tier_plot', and 'custom_test_tier_df' session states.
    """

    if st.button("Delete Custom Test-Format Tier Table"):
        st.session_state["custom_test_tier_list"] = []
        st.session_state['show_test_tier_plot'] = False
        st.session_state.custom_test_tier_df = None
        st.session_state.temp_custom_lab_specific_test_by_laboratory_section_df  = None
        st.session_state.custom_lab_specific_test_by_laboratory_section_df  = None

        msg = st.toast('Deleting Custom Test Tier...')
        time.sleep(0.7)
        msg.toast('Deleted 🗑️')
        time.sleep(0.7)
        st.rerun()


def save_current_coustom_test_tier_df():
    """
    Saves the current custom test tier list as a DataFrame in the session state.
    If the list is not empty, it saves the DataFrame and displays a success message.
    If the list is empty, it shows a warning toast message.
    """

    if st.button("Save Custom Test-Format Tier Table"):
        if len(st.session_state.custom_test_tier_list):
            st.session_state.custom_test_tier_df = pd.DataFrame(st.session_state.custom_test_tier_list)

            msg = st.toast('Saving/Applying Custom Test Tier...')
            time.sleep(0.7)
            msg.toast('Saved & Applied ✅ ')

        else:
            st.toast("Could Not Find Custom Test Tier Dataframe")


def add_sidebar(): 
    with st.sidebar:
        st.markdown("""
            # Custom Test-Format Tier Page

            Welcome to the **Custom Test-Format Tier** page. This page allows you to create, manage, and visualize a custom test-format tier dataset for diagnostic purposes. You can build a test-formate table by adding individual records, uploading a CSV file, or directly editing the existing dataset. The main features and functionalities of this page are as follows:

            ### Key Features:
            - **Add New Test-Format Records:**
              - Manually add new test-format records by specifying the test-format and test tier (:blue-background[Primary], :blue-background[Secondary], :blue-background[Tertiary]).

            - **Upload Custom Test-Format Tier CSV:**
              - Upload a pre-developed dataset in CSV format. The uploaded file must contain columns :blue-background['test_format'] and :blue-background['custom_test_tier'].

            - **Display and Edit Test-Format Table:**
              - View and edit the current test-format table. Mark records for deletion directly within the table.

            - **Save and Delete Test-Format Table:**
              - Save the current custom test table or delete the entire table if needed.

            - **Render Custom Test-Format Tier Plot:**
              - Once the test table is built or uploaded, render a custom test-format tier plot to visualize the distribution of test-format tiers across different health facility tiers. Redraw or delete the plot as needed.

            ### Instructions:
            1. **Add a New Test-Format Record:**
              - Use the form provided to select the test-format and tier, then click 'Add' to append the new record to the table.

            2. **Upload a Custom Test-Format Tier CSV:**
              - Use the file uploader to select and upload your CSV file. Ensure that your file contains the required columns.

            3. **Display and Edit Test-Format Table:**
              - View the current test-format table and mark any records for deletion. Changes will be reflected instantly.

            4. **Save or Delete the Test-Format Table:**
              - Use the provided buttons to save the current table for future use or delete the existing table to start fresh.

            5. **Render and Manage Plot:**
              - Click 'Render Custom Test Tier Plot' to visualize your data. You can also redraw or delete the plot using the respective buttons.

            This page empowers you to customize and visualize test tiers efficiently, supporting better diagnostic planning and resource allocation.
        """)
