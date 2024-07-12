import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st
from data.database import get_db
import time


@st.cache_data(ttl=3600)
def retrieve_gbd_conditions():
    """
    Fetches and returns a sorted list of condition names from the 'conditions' table
    where the 'lancet_gbd' field is 'Yes'. The data is cached for 3600 seconds.
    """

    from data.models import Condition as condition_table
    db = next(get_db())

    try:
        query = db.query(condition_table.condition_name)
        conditions = query.filter(condition_table.lancet_gbd == 'Yes').all()
    finally:
        db.close()

    return sorted([_[0] for _ in conditions])


def create_condition_plot(df):
    """
    Creates and returns a condition level plot based on the given DataFrame.
    
    Parameters:
    df (DataFrame): DataFrame containing 'conditionname', 'conditionlevel', and 'custom_condition_tier' columns.
    
    Returns:
    Figure: A matplotlib figure object representing the condition levels by health facility tier.
    """

    # Define the color mapping
    color_map = {
        "triage": "lightyellow",
        "moderate": "orange",
        "severe": "brown",
        "not applicable": "white"
    }

    # Define the tiers and conditions
    tiers = ["Primary", "Secondary", "Tertiary"]
    conditions = df["conditionname"].unique()

    # Create a mapping for condition levels to ensure specific order
    level_order = {"triage": 1, "moderate": 2, "severe": 3}

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 8))

    # Draw the grid and rectangles
    for i, condition in enumerate(conditions):
        for j, tier in enumerate(tiers):
            # Get the condition levels for this cell
            cell_data = df[(df["conditionname"] == condition) & (df["custom_condition_tier"] == tier)]
            
            if not cell_data.empty:
                levels = sorted(cell_data["conditionlevel"].values, key=lambda x: level_order[x])
                num_levels = len(levels)
                for k, level in enumerate(levels):
                    rect = patches.Rectangle(
                        (j + k / num_levels, i), 1 / num_levels, 1,
                        linewidth=1, edgecolor='black', facecolor=color_map[level]
                    )
                    ax.add_patch(rect)
            else:
                # Add an empty rectangle for "not applicable" cases
                rect = patches.Rectangle(
                    (j, i), 1, 1,
                    linewidth=1, edgecolor='black', facecolor=color_map["not applicable"]
                )
                ax.add_patch(rect)

    # Set the axis limits and labels
    ax.set_xlim(0, len(tiers))
    ax.set_ylim(0, len(conditions))
    ax.set_xticks([0.5, 1.5, 2.5])
    ax.set_xticklabels(tiers)
    ax.set_xlabel("Health Facility Tier")
    ax.set_title("Condition Levels by Health Facility Tier")

    # Adjust y-tick positions to the center of each row
    ytick_positions = [i + 0.5 for i in range(len(conditions))]
    ax.set_yticks(ytick_positions)
    ax.set_yticklabels(conditions)
    ax.set_ylabel("Condition Name")

    legend_elements = [
        patches.Patch(facecolor='lightyellow', edgecolor='black', label='Triage'),
        patches.Patch(facecolor='orange', edgecolor='black', label='Moderate'),
        patches.Patch(facecolor='brown', edgecolor='black', label='Severe'),
        patches.Patch(facecolor='white', edgecolor='black', label='Not applicable')
    ]
    ax.legend(handles=legend_elements, title="Condition Level", loc='center left', bbox_to_anchor=(1, 0.5))

    # Show the plot
    plt.gca().invert_yaxis()
    plt.tight_layout(rect=[0, 0, 0.85, 1])
    return fig


def add_new_condition():
    """
    Adds a new condition to the custom condition list stored in the session state.
    The new condition is added based on the current values of 'conditionname',
    'conditionlevel', and 'custom_condition_tier' in the session state.
    """
    st.session_state.custom_condition_list.append(
        {
            "conditionname": st.session_state.conditionname,
            "conditionlevel": st.session_state.conditionlevel,
            "custom_condition_tier": st.session_state.custom_condition_tier,
        }
    )

def delete_callback():
    """
    Callback function to delete rows from the custom condition list based on user interaction.
    If the 'delete' checkbox is checked for a row, that row is removed from the custom condition list.
    """

    edited_rows = st.session_state["data_editor"]["edited_rows"]
    for idx, value in edited_rows.items():
        if ('delete' in value.keys()) and (value["delete"] is True):
            st.session_state["custom_condition_list"].pop(idx)
        else:
            for k,v in value.items():
                st.session_state["custom_condition_list"][idx][k] = v



def display_custom_condition_df():
    """
    Displays the custom condition list as a data editor in Streamlit.
    Allows users to view and mark rows for deletion. The 'delete' column is added
    to allow users to mark rows for deletion.
    """

    custom_condition_df = pd.DataFrame(st.session_state["custom_condition_list"])
    column_config = {
        'conditionname': st.column_config.Column(
            disabled=True,
            help='Condition Name'
        ),
        'conditionlevel': st.column_config.SelectboxColumn(
            help='Condition Level',
            options=['triage','moderate','severe'],
            required=True,
        ),
        'custom_condition_tier': st.column_config.SelectboxColumn(
            help='Custom Condition Tier',
            options=['Primary','Secondary','Tertiary'],
            required=True,
        )
    }
    custom_condition_df["delete"] = False

    # Make Delete be the first column
    custom_condition_df = custom_condition_df[
        ["delete"] + custom_condition_df.columns[:-1].tolist()
    ]

    st.data_editor(
        custom_condition_df,
        key="data_editor",
        on_change=delete_callback,
        hide_index=False,
        column_config=column_config,
        use_container_width=True
    )


def delete_current_coustom_df():
    """
    Deletes the current custom condition table from the session state.
    Resets the 'custom_condition_list', 'show_plot', and 'custom_condition_df' session states.
    """

    if st.button("Delete Current Custom Condition Table"):
        st.session_state["custom_condition_list"] = []
        st.session_state['show_plot'] = False
        st.session_state.custom_condition_df = None

        msg = st.toast('Deleting Custom Condition Level...')
        time.sleep(0.7)
        msg.toast('Deleted 🗑️')
        time.sleep(0.7)
        st.rerun()


def save_current_coustom_df():
    """
    Saves the current custom condition list as a DataFrame in the session state.
    If the list is not empty, it saves the DataFrame and displays a success message.
    If the list is empty, it shows a warning toast message.
    """

    if st.button("Save Current Custom Condition Table"):
        if len(st.session_state.custom_condition_list):
            st.session_state.custom_condition_df = pd.DataFrame(st.session_state["custom_condition_list"])
            msg = st.toast('Saving/Applying Custom Condition Level...')
            time.sleep(0.7)
            msg.toast('Saved & Applied ✅ ')

        else:
            st.toast("Could Not Find Custom Condition Level Dataframe")
def add_sidebar():
    with st.sidebar:
        st.markdown("""
                    # Custom Condition Tier Page

                    Welcome to the **Custom Condition Tier** page. This page allows users to create, manage, and visualize a custom condition tier dataset for diagnostic purposes. Here, you can build a condition table by adding individual records, uploading a CSV file, or directly editing the existing dataset. The main features and functionalities of this page are as follows:

                    ### Key Features:
                    - **Add New Condition Records:**
                    - You can manually add new condition records by specifying the condition name, condition level (triage, moderate, severe, not applicable), and condition tier (Primary, Secondary, Tertiary).

                    - **Upload Custom Condition Tier CSV:**
                    - If you have a pre-existing dataset, you can upload it in CSV format. The uploaded file must contain columns 'conditionname', 'conditionlevel', and 'custom_condition_tier'.

                    - **Display and Edit Condition Table:**
                    - The current condition table is displayed for easy viewing and editing. You can mark records for deletion directly within the table.

                    - **Save and Delete Condition Table:**
                    - You can save the current custom condition table or delete the entire table if needed.

                    - **Render Custom Condition Tier Plot:**
                    - Once the condition table is built or uploaded, you can render a custom condition tier plot to visualize the distribution of condition levels across different health facility tiers. You can redraw or delete the plot as needed.

                    ### Instructions:
                    1. **Add a New Condition Record:**
                    - Use the form provided to select the condition name, level, and tier, then click 'Add' to append the new record to the table.

                    2. **Upload a Custom Condition Tier CSV:**
                    - Use the file uploader to select and upload your CSV file. Ensure that your file contains the required columns.

                    3. **Display and Edit Condition Table:**
                    - View the current condition table and mark any records for deletion. Changes will be reflected instantly.

                    4. **Save or Delete the Condition Table:**
                    - Use the provided buttons to save the current table for future use or delete the existing table to start fresh.

                    5. **Render and Manage Plot:**
                    - Click 'Render Custom Condition Tier Plot' to visualize your data. You can also redraw or delete the plot using the respective buttons.

                    This page empowers users to customize and visualize condition tiers efficiently, supporting better diagnostic planning and resource allocation.
                    """)
