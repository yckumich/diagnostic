import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st
from data.database import get_view_df
import time

def retrieve_gbd_test_formats():
    view_df = get_view_df()
    condition_names_list = sorted(pd.read_csv("static/conditions.csv").query("lancet_gbd == 'Yes'")['condition_name'].to_list(), key=str.casefold)
    test_format_list = set(view_df[view_df['conditionname'].isin(condition_names_list)]['test_format'].dropna())
    del view_df

    return sorted(test_format_list, key=str.casefold)

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
    df['tier_index'] = df['custom_test_tier'].map(tier_indices)
    df = df.sort_values(by=['tier_index', 'test_format'], key=lambda col: col.str.casefold() if col.name == 'test_format' else col).reset_index(drop=True)

    # Extract the sorted test names
    tests = df["test_format"].unique()

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, int(df['test_format'].nunique()/3.5)))

    # Draw the grid and rectangles
    for i, test in enumerate(tests):
        # Determine the highest applicable tier for the current test
        highest_tier = None
        for tier in tiers:
            if not df[(df["test_format"] == test) & (df["custom_test_tier"] == tier)].empty:
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


##---------
def add_new_test_tier():
    """
    Adds a new test tier record to the custom test tier list stored in the session state.
    The new record is added based on the current values of 'test_format' and 'custom_test_tier' in the session state.
    """
    st.session_state.custom_test_tier_list.append(
        {
            "test_format": st.session_state.test_format,
            "custom_test_tier": st.session_state.custom_test_tier,
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
        'test_format': st.column_config.Column(
            disabled=True,
            help='Test Format'
        ),
        'custom_test_tier': st.column_config.SelectboxColumn(
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
            # Custom Test Tier Page

            Welcome to the **Custom Test Tier** page. This page allows users to create, manage, and visualize a custom test tier dataset for diagnostic purposes. Here, you can build a test table by adding individual records, uploading a CSV file, or directly editing the existing dataset. The main features and functionalities of this page are as follows:

            ### Key Features:
            - **Add New Test Records:**
              - You can manually add new test records by specifying the test format and test tier (Primary, Secondary, Tertiary).

            - **Upload Custom Test Tier CSV:**
              - If you have a pre-developed dataset, you can upload it in CSV format. The uploaded file must contain columns 'testname' and 'custom_test_tier'.

            - **Display and Edit Test Table:**
              - The current test table is displayed for easy viewing and editing. You can mark records for deletion directly within the table.

            - **Save and Delete Test Table:**
              - You can save the current custom test table or delete the entire table if needed.

            - **Render Custom Test Tier Plot:**
              - Once the test table is built or uploaded, you can render a custom test tier plot to visualize the distribution of test tiers across different health facility tiers. You can redraw or delete the plot as needed.

            ### Instructions:
            1. **Add a New Test Record:**
              - Use the form provided to select the test format and tier, then click 'Add' to append the new record to the table.

            2. **Upload a Custom Test Tier CSV:**
              - Use the file uploader to select and upload your CSV file. Ensure that your file contains the required columns.

            3. **Display and Edit Test Table:**
              - View the current test table and mark any records for deletion. Changes will be reflected instantly.

            4. **Save or Delete the Test Table:**
              - Use the provided buttons to save the current table for future use or delete the existing table to start fresh.

            5. **Render and Manage Plot:**
              - Click 'Render Custom Test Tier Plot' to visualize your data. You can also redraw or delete the plot using the respective buttons.

            This page empowers users to customize and visualize test tiers efficiently, supporting better diagnostic planning and resource allocation.
        """)