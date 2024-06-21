import streamlit as st
from data.database import engine, Base
from utils.utils import *
import pandas as pd
from typing import Dict
from st_aggrid import AgGrid, GridUpdateMode, AgGridTheme


# Create the database tables (if they don't already exist)
Base.metadata.create_all(bind=engine)
agg_filter_selection = dict()


def create_filter_expander(expander_title:str, subfilter_map:dict) -> Dict:
    selected_option_map = {k:[] for k in subfilter_map.keys()}
    with st.expander(expander_title):
        for subfilter_title, options_list in subfilter_map.items():
            selected_option_map[subfilter_title] = st.multiselect(subfilter_title, options_list, default=[])
    return selected_option_map


def create_detail_expander(detail_title:str, details:List):
    if detail_title != 'testname':
        with st.expander("**"+detail_title+"**"):
            markdown_string = ''
            for detail in details:
                markdown_string += "- " + str(detail) + "\n"
            st.markdown(markdown_string)

def add_sidebar(filter_map):
    with st.sidebar:
        st.header('Filters')
        for main_filter in filter_map:
            # selected_option_map = create_expander(main_filter, filter_map[main_filter])
            agg_filter_selection[main_filter] = create_filter_expander(main_filter, filter_map[main_filter])

        st.divider()  
        with st.expander("Current Filter Selection"):
            st.json(agg_filter_selection)    

    return agg_filter_selection


def display_test_details(test_details):
    for key, value in test_details.items():
        st.write(f"**{key}**: {value}")


def compare_lists(data: dict) -> pd.DataFrame:
    labels = list(data.keys())
    lists = list(data.values())

    # Determine the maximum length of the lists
    max_length = max(len(lst) for lst in lists)
    
    # Pad the shorter lists with empty strings
    extended_lists = [lst + [""] * (max_length - len(lst)) for lst in lists]
    
    # Transpose the lists to get rows
    rows = list(zip(*extended_lists))
    
    # Function to sort items in each row in descending order, handling None values
    def sort_row(row):
        return sorted(row, key=lambda x: (x is None, str(x)), reverse=True)
    
    # Sort each row and replace None with an empty string
    sorted_rows = [sort_row([item if item is not None else "" for item in row]) for row in rows]
    
    # Create a DataFrame for comparison
    comparison_df = pd.DataFrame(sorted_rows, columns=labels)
    return comparison_df

# Function to create comparison expanders with dataframes
def create_comparison_expandable(data: dict):
    # Extract all test details
    test_details = list(next(iter(data.values())).keys())
    
    # Iterate over each test detail
    for detail in test_details:
        # Create a dictionary to store lists for each test
        detail_dict = {test: data[test][detail] for test in data}
        
        # Use compare_lists to create the comparison DataFrame
        comparison_df = compare_lists(detail_dict)
        
        # Create an expander for each test detail
        with st.expander(label=detail):
            st.dataframe(comparison_df)

def main():

    st.set_page_config(
        page_title="EDL Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    local_css("style.css")

    filter_map = get_filter()
    selection = add_sidebar(filter_map=filter_map)
    selected_test_df = convert_selection_to_df(selection)
    unique_test_df = (selected_test_df[['testname']]
                      .drop_duplicates(subset=['testname'])
                      .reset_index(drop=True)
                      .sort_values(by='testname'))

    st.divider()  

    test_list_col, test_detail_col = st.columns([0.25, 0.75], gap="small")
    
    ## passing the first 100 rows to build the grid option
    grid_option = build_grid_option(unique_test_df)
        
    with test_list_col:
        st.header("Test Names")

        grid_table = AgGrid(
            data=unique_test_df,
            gridOptions=grid_option,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            height=1000,
            theme=AgGridTheme.MATERIAL
        )

        sel_row = grid_table['selected_rows']

        if isinstance(sel_row, pd.DataFrame):
            with test_detail_col:
                st.header('Test Detail')
                st.markdown("""<div style="height:23px;"></div>""", unsafe_allow_html=True)
                st.divider()
                test_name_list = list(sel_row['testname'])
                
                if len(test_name_list) == 1 :
                    test_df = selected_test_df[selected_test_df['testname'] == test_name_list[0]]
                    test_detail = create_test_detail(test_df)
                    for detail_title, details in test_detail.items():
                        create_detail_expander(detail_title, details)
                else:
                    test_df = selected_test_df[selected_test_df['testname'].isin(test_name_list)]
                    for col_name, test_detail_df in iter(generate_test_detail_dataframe(test_df)):
                        with st.expander(label=col_name):
                            st.dataframe(
                                test_detail_df,
                                use_container_width=True
                            )
                    


if __name__ == "__main__":
    main()