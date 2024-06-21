import streamlit as st
import pandas as pd

# Function to compare multiple lists and create a DataFrame
def compare_lists(data: dict) -> pd.DataFrame:
    labels = list(data.keys())
    lists = list(data.values())

    # Determine the maximum length of the lists
    max_length = max(len(lst) for lst in lists)
    
    # Pad the shorter lists with empty strings
    extended_lists = [lst + [""] * (max_length - len(lst)) for lst in lists]
    
    # Transpose the lists to get rows
    rows = list(zip(*extended_lists))
    
    # Function to sort items in each row in descending order
    def sort_row(row):
        return sorted(row, reverse=True)
    
    # Sort each row
    sorted_rows = [sort_row(row) for row in rows]
    
    # Create a DataFrame for comparison
    comparison_df = pd.DataFrame(sorted_rows, columns=labels)
    return comparison_df

# Example input data
input_data = {
    "Coagulation": [
        "Pathophysiology", "DiffDiagnosis", "Complication", "CoMorbidity",
        "Toxicity", "Dosing/Safety", "Diagnosis", "Monitoring"
    ], 
    "Fibrinogen":[
        "DiffDiagnosis", "Complication", "Toxicity", "Dosing/Safety", "Diagnosis", "Monitoring"
    ], 
    "Another Test": [
         "Diagnosis", "Monitoring", "Toxicity", "Dosing/Safety", "Pathophysiology"
    ]
}

# Create the comparison DataFrame
comparison_df = compare_lists(input_data)

# Display the comparison table in Streamlit with a fixed height for scrolling
st.title("Comparison of Test Reasons")
st.dataframe(comparison_df, height=400)  # Adjust the height as needed
