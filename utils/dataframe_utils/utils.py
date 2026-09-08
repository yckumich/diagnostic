from utils.dataframe_utils.filter import high_level_filter_map
from st_aggrid.grid_options_builder import GridOptionsBuilder
from data.database import get_view_df
from typing import Dict, List, Any
import streamlit as st
import pandas as pd
import zipfile
import io

def convert_query_to_df(query_stmt:str) -> pd.DataFrame:
    view_df = get_view_df()
    # print('view_df.shape in convert_query_to_df: ', view_df.shape)
    if query_stmt != "":
        return view_df.query(query_stmt)
    else:
        return view_df


def extract_unique_values(df: pd.DataFrame, 
                          filter_map: Dict[str, Dict[str, str]], 
                          filter_key: str) -> Dict[str, List]:
    """
    Creates a dictionary of unique values for each sub-filter associated with a given main filter.
    """
    unique_values = {}
    
    for sub_filter, column in filter_map[filter_key].items():
        unique_values[sub_filter] = sorted(list(df[column].unique()),  key=lambda x: (x is None, x))
        
    return unique_values


def create_filter_map(df:pd.DataFrame, 
                      filter_map:dict) -> Dict[str, Dict[str, List]]:
    """
    Creates a comprehensive dictionary of unique values for each sub-filter associated with all main filters.
    """
    complete_filter = {}
    
    for main_filter in filter_map.keys():
        complete_filter[main_filter] = extract_unique_values(df, filter_map, main_filter)

    return complete_filter


def get_filter()-> Dict:

    view_df = get_view_df()    
    return create_filter_map(view_df, high_level_filter_map)


@st.cache_data(ttl=3600)
def convert_selection_to_filter(selection: Dict[str,Dict[str,List[str]]]) -> Dict[str,List[str]]:
    """
    Convert a nested dictionary of user selections into a filter dictionary for database querying.
    """
    global high_level_filter_map

    title_to_col = {k: v for d in [v for v in high_level_filter_map.values()] for k, v in d.items()}
    selection_to_filter = dict()
    
    for ll_filter in selection.values():
        for k, v in ll_filter.items():
            if v:
                selection_to_filter[title_to_col[k]] = v
    
    return selection_to_filter


def convert_filter_to_query(filters:Dict[str,List[str]]) -> str:
    return " and ".join([f"{k} in {v}" for k,v in filters.items()])


# @st.cache_data(ttl=3600)
##THIS CAUSE THE PROBLEM!!! OF NOT LETTING IT TO RUN !!
def convert_selection_to_df(selection: Dict[str,Dict[str,List[str]]]) -> pd.DataFrame:
    """
    Convert a nested dictionary of user selections into a pandas DataFrame by applying the 
    corresponding filters and executing the query.
    """
    filters = convert_selection_to_filter(selection=selection)
    # print("filters: ", filters)
    query_w_filter = convert_filter_to_query(filters=filters)
    # print("query_w_filter: ", query_w_filter)
    
    return convert_query_to_df(query_w_filter)


def build_grid_option(df:pd.DataFrame,
                      pagination_size:int=50, 
                      selection_mode='multiple'):
    """
    Builds and configures grid options for displaying a DataFrame using st_aggrid.
    """
    gd = GridOptionsBuilder.from_dataframe(df)

    gd.configure_pagination(
        enabled=False,
        paginationPageSize=pagination_size, 
        paginationAutoPageSize=False,
    )
    gd.configure_default_column(
        editable=False,
        groupable=True
    )
    gd.configure_selection(
        selection_mode=selection_mode, 
        use_checkbox=False
    )
    return gd.build()


@st.cache_resource(ttl=3600)
def get_unique_values(input_list: List[Any]) -> List[Any]:
    """
    This function takes a list containing various types including float('nan') and returns a new list
    with unique values and compresses all 'nan' values into a single occurrence.
    """

    return list(set(map(str, input_list)))
    
    
@st.cache_resource(ttl=3600)
def create_test_detail(df:pd.DataFrame) -> Dict:
    """
    df contains dataframe of a single test
    """
    col_to_unique_map = dict()
    for col in df.columns:
        col_to_unique_map[col] = get_unique_values(list(df[col]))
    
    return col_to_unique_map


def create_sorted_dataframe(data: dict[str,List]) -> pd.DataFrame:
    """
    Converts a dictionary of lists into a sorted DataFrame,
    where each list is padded to the same length and sorted in descending order.
    """
    def sort_row(row):
        return sorted(row, key=lambda x: (x != "", str(x)), reverse=True)
    
    # labels = list(data.keys())
    lists = list(data.values())
    
    # Determine the maximum length of the lists
    max_length = max(len(lst) for lst in lists)
    
    # Pad the shorter lists with empty strings
    for label in data.keys():
        num_pad = max_length - len(data[label])
        data[label] = data[label] + [""] * num_pad
    
    sorted_data = {label:sort_row(data[label]) for label in data.keys()}
    
    return pd.DataFrame(sorted_data)
    
    
def generate_test_detail_dataframe(test_df:pd.DataFrame):
    """
    Processes a DataFrame of test details to generate sorted DataFrames for each
    column (excluding 'testname'), mapping tests to unique details for each specified column.
    The function groups the input data by 'testname', constructs a dictionary of test details, 
    and then yields a tuple containing the column name and the corresponding sorted DataFrame.
    """
    
    test_to_col_to_detail = dict()
    for test, df in test_df.groupby(by='testname'):
        test_to_col_to_detail[test] = create_test_detail(df)

    test_list = test_to_col_to_detail.keys()
    col_names = list(next(iter(test_to_col_to_detail.values())).keys())
    col_names.remove('testname')
    
    for col in col_names:
        test_to_detail_list = {test: list(set(map(str,test_to_col_to_detail[test][col]))) for test in test_list}
        yield col, create_sorted_dataframe(test_to_detail_list)


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


# def generate_zip(selected_filters, dataframes):
def generate_zip(dataframes:List[Any]):
    # Create a byte stream to hold the zip file in memory
    zip_buffer = io.BytesIO()
    
    # Create a new zip file
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zf:

        # Add each dataframe to the zip file
        for title, df in dataframes:
            if not df.empty and title in ['Test By Condition', 'Test By Laboratory Section', 'Format By Test', 'Format and Tiers']:
                # print(f'generating zip for {title}')
                df_bytes = df.to_csv(index=False).encode('utf-8')
                zf.writestr(f'{title}.csv', df_bytes)
        
    # Seek to the beginning of the stream
    zip_buffer.seek(0)
    
    return zip_buffer

def collect_and_generate_zip(collected_dataframes):
    zip_buffer = generate_zip(collected_dataframes)

    # Provide a download link
    return zip_buffer


sidebar_instruction = """
**Essential Diagnostics Explorer**  
Welcome to the Essential Diagnostics Explorer. This page allows you to filter and explore diagnostics and their associations based on various conditions, medicines, and other attributes. It includes diagnostics from the WHO Essential Diagnostics List as well as other diagnostics used to support WHO Essential Medicines. Follow the steps below to make the most of this page:

**How to Use This Page:**
1. **Filters:** Select your desired filters from each dropdown to refine the diagnostics displayed on the dashboard.
    - **Diagnostic:** Filter by diagnostic features.
    - **Medicine:** Filter by associated medicines.
    - **Condition:** Filter by associated conditions.
    - **WHO EDL/EML:** Filter by features of the WHO Essential Diagnostics List or Essential Medicines List.
    - **Lancet:** Filter by features from the Lancet study (see Home).
2. **Current Filter Selection:**
    - This section displays the current filters you have selected. Expand it to review if you want to ensure your selections are correct.
3. **Diagnostic Name Panel:**
    - On the far right panel of the dashboard, you'll see a list of diagnostic names that match your selected filters (and any additional filters created and applied in the Set Condition Tiers and Set Diagnostic-Format Tiers pages). Click on any diagnostic name to further refine your dashboard.
4. **Tabs Panel:**
    - The main panel of the page is divided into multiple tabs:
        - **Diagnostic Details:** Displays diagnostics by domain (e.g., laboratory section) and diagnostic formats.
        - **Diagnostic By Condition:** Displays diagnostics associated with different conditions (e.g., diseases).
        - **Diagnostic By Medicine:** Displays diagnostics associated with different medicines (either due to medicines associated with conditions for which the diagnostic is indicated, or due to medicine-related diagnostic indications, e.g. for toxicity effects).
        - **Diagnostic By Med And Cond:** Displays diagnostics with associated medicines and conditions (use this to view diagnostic indications at the most granular level).
        - **Medicine Indications:** Displays the medicines indicated for different conditions.
5. **Condition and Diagnostic-Format Tier Status:**
    - Indicators at the top show whether custom Condition Tiers and Diagnostic-Format Tiers filters are applied. This helps to know if additional custom filters are in effect.
6. **Interacting with the Essential Diagnostics Explorer:**
    - The Essential Diagnostics Explorer is useful for viewing and downloading detailed associations.
    - Use the left sidebar filters to adjust the data dynamically.
    - Click on specific diagnostics in the Diagnostic Name column to filter further. Use shift-select and control-select for multiple selections. Control-select on a selected diagnostic will deselect it.
    - Switch between tabs to get different views and detailed insights into the diagnostics.
    - Each table in the dashboard can be downloaded as CSV files by hovering over the headers.
    - While the Condition Tiers and Diagnostic-Format Tiers filters will change the content of these Essential Diagnostics Explorer tables, filtering within the Explorer (left or right panels) will not affect the Diagnostic Network Planner results.
"""