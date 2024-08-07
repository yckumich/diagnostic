import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import streamlit as st
import time

CONDITION_LEVELS = ["triage", "moderate", "severe", "not applicable"]
CONDITION_TIERS = ["Primary", "Secondary", "Tertiary"]
ESSENTIAL_COLS = ['conditionname', 'conditionlevel', 'custom_condition_tier']


@st.cache_data(ttl=3600)
def retrieve_gbd_conditions():
    """
    Fetches and returns a sorted list of condition names from the 'conditions' table
    where the 'lancet_gbd' field is 'Yes'. The data is cached for 3600 seconds.
    """

    return sorted(pd.read_csv("static/conditions.csv").query("lancet_gbd == 'Yes'")['condition_name'].to_list(), key=str.casefold)

GDB_CONDITION_LIST = retrieve_gbd_conditions()

def process_condition_tiers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Processes the input DataFrame to ensure that each condition has the appropriate tiers (Primary, Secondary, Tertiary) based on the condition level.
    
    Parameters:
    df (pd.DataFrame): DataFrame containing columns 'conditionname', 'conditionlevel', and 'custom_condition_tier'.
    
    Returns:
    pd.DataFrame: A DataFrame with processed condition tiers ensuring that if a condition has a secondary or tertiary tier, 
                  it also includes the necessary primary and/or secondary tiers as per the hierarchical order.
    """
    
    # Define the order for tiers and levels and other variables 
    tier_order = {"Primary": 1, "Secondary": 2, "Tertiary": 3}
    level_order = {"triage": 1, "moderate": 2, "severe": 3}
    condition_df_dict_list = list()
    final_df_dict_list = list()
    secondary_filled_tertiary = False
    
    # Group by condition name and condition level to sort custom condition tier
    for condition_name, condition_df in df.groupby(by='conditionname'):
        for condition_level, condition_tier_df in condition_df.groupby('conditionlevel'):
            condition_df_dict_list.append(
                {
                    'conditionname': condition_name,
                    'conditionlevel': condition_level,
                    'custom_condition_tier': sorted(
                        condition_tier_df['custom_condition_tier'].values, 
                        key=lambda x: tier_order[x])[0]
                }
            )
    
    processed_df = pd.DataFrame.from_dict(condition_df_dict_list)
    
    # Ensure that each condition has the appropriate tiers
    for conditionname, condition_df in processed_df.groupby(by='conditionname'):
        if len(set(condition_df['custom_condition_tier'])) == 3:
            for i,row in condition_df.iterrows():
                final_df_dict_list.append(
                    {
                        'conditionname':conditionname,
                        'conditionlevel':row['conditionlevel'],
                        'custom_condition_tier':row['custom_condition_tier'],
                    }
                )
        else:
            if 'Tertiary' in set(condition_df['custom_condition_tier']):
                df_w_tertiary = condition_df[condition_df['custom_condition_tier'] == 'Tertiary']
                for i,row in df_w_tertiary.iterrows():
                    final_df_dict_list.append(
                        {
                            'conditionname':conditionname,
                            'conditionlevel':row['conditionlevel'],
                            'custom_condition_tier':row['custom_condition_tier'],
                        }
                    )
                    
            if 'Secondary' in set(condition_df['custom_condition_tier']):
                df_w_secondary = condition_df[condition_df['custom_condition_tier'] == 'Secondary']
                for i,row in df_w_secondary.iterrows():
                    final_df_dict_list.append(
                        {
                            'conditionname':conditionname,
                            'conditionlevel':row['conditionlevel'],
                            'custom_condition_tier':row['custom_condition_tier'],
                        }
                    )   
                highest_condition_level_in_secondary = sorted(
                    condition_df[condition_df['custom_condition_tier'] == 'Secondary']['conditionlevel'].values,
                    key=lambda x: level_order[x]
                )[-1]
                
                if 'Tertiary' not in set(condition_df['custom_condition_tier']):
                    final_df_dict_list.append(
                        {
                            'conditionname':conditionname,
                            'conditionlevel':highest_condition_level_in_secondary,
                            'custom_condition_tier': 'Tertiary',
                        }
                    )
                    secondary_filled_tertiary = True
            
            if 'Primary' in set(condition_df['custom_condition_tier']):
                df_w_primary = condition_df[condition_df['custom_condition_tier'] == 'Primary']
                for i,row in df_w_primary.iterrows():
                    final_df_dict_list.append(
                        {
                            'conditionname':conditionname,
                            'conditionlevel':row['conditionlevel'],
                            'custom_condition_tier':row['custom_condition_tier'],
                        }
                )                
                    
                highest_condition_level_in_primary = sorted(
                    condition_df[condition_df['custom_condition_tier'] == 'Primary']['conditionlevel'].values,
                    key=lambda x: level_order[x]
                )[-1]
                
                if 'Secondary' not in set(condition_df['custom_condition_tier']):
                    final_df_dict_list.append(
                        {
                            'conditionname':conditionname,
                            'conditionlevel':highest_condition_level_in_primary,
                            'custom_condition_tier': 'Secondary',
                        }
                    )    
                if ((not secondary_filled_tertiary) and 
                    ('Tertiary' not in set(condition_df['custom_condition_tier']))):
                    final_df_dict_list.append(
                        {
                            'conditionname':conditionname,
                            'conditionlevel':highest_condition_level_in_primary,
                            'custom_condition_tier': 'Tertiary',
                        }
                    )             
    
    return pd.DataFrame.from_dict(final_df_dict_list)
        
        
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
    conditions = sorted(df["conditionname"].unique(), key=str.casefold)

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


def display_add_condition_form():
    st.write("### Add a New Custom Condition Instance ")
    with st.form("new_condition", clear_on_submit=True):
        st.selectbox("Condition Name", GDB_CONDITION_LIST, key="conditionname")
        st.selectbox("Condition Level", CONDITION_LEVELS, key="conditionlevel")
        st.selectbox("Condition Tier", CONDITION_TIERS, key="custom_condition_tier")
        st.form_submit_button("Add", on_click=add_new_condition)


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


def handle_custom_condition_file_upload(condition_level_csv):
    
    try:
        uploaded_df = pd.read_csv(condition_level_csv)
        uploaded_df_cols = list(uploaded_df.columns)
        if set(uploaded_df_cols) != set(ESSENTIAL_COLS):
            st.warning(
                body="columns 'conditionname', 'conditionlevel', 'custom_condition_tier' must be presented in the uploaded csv file",
                icon="⚠️"
            )
        else:
            st.session_state["custom_condition_list"] = uploaded_df.to_dict(orient='records')
            st.session_state['show_plot'] = False
            st.rerun()

    except Exception as e:
        st.error(f"Error uploading file: {e}")


def upload_custom_condition_csv():
    st.write("### Upload a Custom Condition Tier CSV")
    condition_level_csv = st.file_uploader("upload a CSV file", type={"csv", "txt"})
    if (condition_level_csv is not None) and (st.button("Upload")):
        handle_custom_condition_file_upload(condition_level_csv)


def render_plot():
    fig = create_condition_plot(
        process_condition_tiers(
            pd.DataFrame(st.session_state["custom_condition_list"])
        )
    )
    st.pyplot(fig)

    st.markdown("""<div style="height:50px;"></div>""", unsafe_allow_html=True)
    _, col1, col2, col3, _ = st.columns([0.23, 0.17, 0.17, 0.2, 0.23], gap='small')
    with col1:
        if st.button('Redraw Plot'):
            st.rerun()
    with col2:
        if st.button('Delete Plot'):
            st.session_state['show_plot'] = False
            st.rerun()
    with col3:
        st.download_button(
            label="Download Table",
            data=pd.DataFrame(st.session_state["custom_condition_list"]).to_csv(index=False),
            file_name='custom_condition_level.csv',
            mime='text/csv',
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
            ## Custom Condition Tier Page

            Welcome to the **Custom Condition Tier** page. This page allows you to create, manage, and visualize a custom condition tier dataset for diagnostic purposes. You can build a condition table by adding individual records, uploading a CSV file, or directly editing the existing dataset. Follow the steps below to use this page effectively:

            ### Key Features:
            - **Add New Condition Records:** Manually add new condition records by specifying the condition name, condition level (triage, moderate, severe), and condition tier (Primary, Secondary, Tertiary).
            - **Upload Custom Condition Tier CSV:** Upload a pre-developed dataset in CSV format. The CSV file must contain the columns :blue-background[conditionname], :blue-background[conditionlevel], and :blue-background[custom_condition_tier].
            - **Display and Edit Condition Table:** View the current condition table and mark records for deletion directly within the table.
            - **Save and Delete Condition Table:** Save the current custom condition table or delete the entire table if needed.
            - **Render Custom Condition Tier Plot:** Visualize the distribution of condition levels across different health facility tiers. You can redraw or delete the plot as needed.

            ### Instructions:
            1. **Add a New Condition Record:**
               - Use the form provided to select the condition name, level, and tier, then click 'Add' to append the new record to the table.
            
            2. **Upload a Custom Condition Tier CSV:**
               - Use the file uploader to select and upload your CSV file. Ensure that your file contains only the required columns: :blue-background[conditionname], :blue-background[conditionlevel], and :blue-background[custom_condition_tier].
            
            3. **Display and Edit Condition Table:**
               - View the current condition table displayed on the left. You can mark records for deletion directly within the table by checking the 'delete' checkbox.
            
            4. **Save or Delete the Condition Table:**
               - Click 'Save Current Custom Condition Table' to save the current table for future use.
               - Click 'Delete Current Custom Condition Table' to delete the existing table and start fresh.
            
            5. **Render and Manage Plot:**
               - Once you have built or uploaded your condition table, click 'Render Custom Condition Tier Plot' to visualize your data.
               - Use the buttons to redraw or delete the plot as needed.
               - You can also download the current table by clicking the 'Download Table' button.

            This page enables efficient customization and visualization of condition tiers, supporting better diagnostic planning and resource allocation.
        """)
