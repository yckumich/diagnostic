import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
import streamlit as st

def plot_condition_levels(df):
    # Define the color mapping
    color_map = {
        "triage": "lightyellow",
        "moderate": "orange",
        "severe": "brown",
        "not applicable": "white"
    }

    # Define the tiers and conditions
    tiers = ["Primary", "Secondary", "Tertiary"]
    conditions = df["condition_name"].unique()

    # Create a mapping for condition levels to ensure specific order
    level_order = {"triage": 1, "moderate": 2, "severe": 3}

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 8))

    # Draw the grid and rectangles
    for i, condition in enumerate(conditions):
        for j, tier in enumerate(tiers):
            # Get the condition levels for this cell
            cell_data = df[(df["condition_name"] == condition) & (df["condition_tier"] == tier)]
            
            if not cell_data.empty:
                levels = sorted(cell_data["condition_level"].values, key=lambda x: level_order[x])
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

# # Example usage in Streamlit
# def main():
#     df_dict ={
#         'condition_name': {
#             0: 'Acute coronary syndrome',
#             1: 'Acute coronary syndrome',
#             2: 'Acute coronary syndrome',
#             3: 'Antenatal care',
#             4: 'Breast cancer, metastatic',
#             5: 'Breast cancer, metastatic',
#             6: 'Breast cancer, metastatic',
#             7: 'COPD',
#             8: 'COPD',
#             9: 'COPD',
#             10: 'Chronic kidney disease',
#             11: 'Chronic kidney disease',
#             12: 'Chronic kidney disease',
#             13: 'Colorectal cancer, metastatic',
#             14: 'Colorectal cancer, metastatic',
#             15: 'Colorectal cancer, metastatic',
#             16: 'Dementia',
#             17: 'Dementia',
#             18: 'Dementia',
#             19: 'Diabetes mellitus',
#             20: 'Diabetes mellitus',
#             21: 'Diabetes mellitus',
#             22: 'Diarrhoea acute invasive bacterial ',
#             23: 'Diarrhoea acute invasive bacterial ',
#             24: 'Diarrhoea acute invasive bacterial ',
#             25: 'HIV',
#             26: 'HIV',
#             27: 'HIV',
#             28: 'Hypertensive heart disease',
#             29: 'Hypertensive heart disease',
#             30: 'Hypertensive heart disease',
#             31: 'Liver cancer',
#             32: 'Liver cancer',
#             33: 'Liver cancer',
#             34: 'Lung cancer, non small cell',
#             35: 'Lung cancer, non small cell',
#             36: 'Lung cancer, non small cell',
#             37: 'Malaria',
#             38: 'Malaria',
#             39: 'Malaria',
#             40: 'Pneumonia community (severe)',
#             41: 'Pneumonia community (severe)',
#             42: 'Pneumonia community (severe)',
#             43: 'Preeclampsia, HELLP',
#             44: 'Preeclampsia, HELLP',
#             45: 'Preeclampsia, HELLP',
#             46: 'Stroke',
#             47: 'Stroke',
#             48: 'Stroke',
#             49: 'Trauma',
#             50: 'Trauma',
#             51: 'Trauma',
#             52: 'Tuberculosis',
#             53: 'Tuberculosis',
#             54: 'Tuberculosis'
#         },
#         'condition_level': {
#             0: 'moderate',
#             1: 'severe',
#             2: 'triage',
#             3: 'triage',
#             4: 'moderate',
#             5: 'severe',
#             6: 'triage',
#             7: 'moderate',
#             8: 'severe',
#             9: 'triage',
#             10: 'moderate',
#             11: 'severe',
#             12: 'triage',
#             13: 'moderate',
#             14: 'severe',
#             15: 'triage',
#             16: 'moderate',
#             17: 'severe',
#             18: 'triage',
#             19: 'moderate',
#             20: 'severe',
#             21: 'triage',
#             22: 'moderate',
#             23: 'severe',
#             24: 'triage',
#             25: 'moderate',
#             26: 'severe',
#             27: 'triage',
#             28: 'moderate',
#             29: 'severe',
#             30: 'triage',
#             31: 'moderate',
#             32: 'severe',
#             33: 'triage',
#             34: 'moderate',
#             35: 'severe',
#             36: 'triage',
#             37: 'moderate',
#             38: 'severe',
#             39: 'triage',
#             40: 'moderate',
#             41: 'severe',
#             42: 'triage',
#             43: 'moderate',
#             44: 'severe',
#             45: 'triage',
#             46: 'moderate',
#             47: 'severe',
#             48: 'triage',
#             49: 'moderate',
#             50: 'severe',
#             51: 'triage',
#             52: 'moderate',
#             53: 'severe',
#             54: 'triage'
#         },
#         'condition_tier': {
#             0: 'Secondary',
#             1: 'Tertiary',
#             2: 'Secondary',
#             3: 'Primary',
#             4: 'Tertiary',
#             5: 'Tertiary',
#             6: 'Primary',
#             7: 'Secondary',
#             8: 'Tertiary',
#             9: 'Primary',
#             10: 'Secondary',
#             11: 'Tertiary',
#             12: 'Primary',
#             13: 'Tertiary',
#             14: 'Tertiary',
#             15: 'Primary',
#             16: 'Secondary',
#             17: 'Tertiary',
#             18: 'Primary',
#             19: 'Secondary',
#             20: 'Tertiary',
#             21: 'Primary',
#             22: 'Secondary',
#             23: 'Tertiary',
#             24: 'Primary',
#             25: 'Primary',
#             26: 'Tertiary',
#             27: 'Primary',
#             28: 'Secondary',
#             29: 'Tertiary',
#             30: 'Primary',
#             31: 'Tertiary',
#             32: 'Tertiary',
#             33: 'Primary',
#             34: 'Tertiary',
#             35: 'Tertiary',
#             36: 'Primary',
#             37: 'Primary',
#             38: 'Tertiary',
#             39: 'Primary',
#             40: 'Primary',
#             41: 'Secondary',
#             42: 'Primary',
#             43: 'Secondary',
#             44: 'Tertiary',
#             45: 'Primary',
#             46: 'Secondary',
#             47: 'Tertiary',
#             48: 'Primary',
#             49: 'Secondary',
#             50: 'Tertiary',
#             51: 'Primary',
#             52: 'Primary',
#             53: 'Tertiary',
#             54: 'Primary'
#         }
#     }
#     df = pd.DataFrame(df_dict)

#     st.title("Condition Levels by Health Facility Tier")

#     # Assuming df is defined elsewhere or imported
#     # df = pd.DataFrame(your_data_here)
#     fig = plot_condition_levels(df)
#     st.pyplot(fig)

# if __name__ == "__main__":
#     main()
import streamlit as st
import pandas as pd

# Initialize the session state
if "condition_data" not in st.session_state:
    st.session_state.condition_data = [
        {"condition_name": "Sample Condition", "condition_level": "moderate", "condition_tier": "Secondary"}
    ]

def new_condition():
    st.session_state.condition_data.append(
        {
            "condition_name": st.session_state.condition_name,
            "condition_level": st.session_state.condition_level,
            "condition_tier": st.session_state.condition_tier,
        }
    )

def delete_row(index):
    del st.session_state.condition_data[index]

# Display the current condition data
st.write("# Condition Table")
condition_df = pd.DataFrame(st.session_state.condition_data)
st.write(condition_df)

# Dropdown to select a row to delete
row_to_delete = st.selectbox("Select row to delete", options=[(i, row["condition_name"], row["condition_level"], row["condition_tier"]) for i, row in enumerate(st.session_state.condition_data)], format_func=lambda x: f"{x[1]} - {x[2]} - {x[3]}")

if st.button("Delete selected row"):
    delete_row(row_to_delete[0])
    st.experimental_rerun()  # Refresh the page to update the table

# Form to add a new condition
st.write("# Add a new condition")
condition_names = [
    "Acute coronary syndrome", "Antenatal care", "Breast cancer, metastatic", "COPD",
    "Chronic kidney disease", "Colorectal cancer, metastatic", "Dementia", "Diabetes mellitus",
    "Diarrhoea acute invasive bacterial", "HIV", "Hypertensive heart disease", "Liver cancer",
    "Lung cancer, non small cell", "Malaria", "Pneumonia community (severe)", "Preeclampsia, HELLP",
    "Stroke", "Trauma", "Tuberculosis"
]
with st.form("new_condition", clear_on_submit=True):
    st.selectbox("Condition Name", condition_names, key="condition_name")
    st.selectbox("Condition Level", ["triage", "moderate", "severe", "not applicable"], key="condition_level")
    st.selectbox("Condition Tier", ["Primary", "Secondary", "Tertiary"], key="condition_tier")
    st.form_submit_button("Submit", on_click=new_condition)

# Button to generate the plot
if st.button("Generate Plot"):
    condition_df = pd.DataFrame(st.session_state.condition_data)
    # Call your plot function here, passing the DataFrame
    # plot = create_condition_plot(condition_df)
    # st.pyplot(plot)

# Button to reset the condition data
if st.button("Reset Data"):
    st.session_state.condition_data = []
    st.experimental_rerun()  # Refresh the page to update the table
