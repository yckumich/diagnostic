from sqlalchemy.orm.query import Query
# from sqlalchemy.orm import Session

from data.database import get_db
from data.models import t_tableau3_t2_tjfs_join_edl_dashadmin as table

from utils.filter import high_level_filter_map
from typing import Dict, List, Any

import streamlit as st
import pandas as pd
import math

from st_aggrid.grid_options_builder import GridOptionsBuilder


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def convert_query_to_df(query:Query, 
                        limit:int=None) -> pd.DataFrame:
    """
    Converts a SQLAlchemy query result into a pandas DataFrame.
    """
    column_names = query.statement.columns.keys()
    query_result = query.limit(limit).all() if limit else query.all()
    
    return pd.DataFrame(columns=column_names, data=query_result)


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


@st.cache_resource(ttl=3600)
def get_filter()-> Dict:
    """
    Retrieves a comprehensive filter dictionary from the database query results.
    """
    global table

    with next(get_db()) as db:
        query = db.query(table)
        df = convert_query_to_df(query, None)
        filter = create_filter_map(df, high_level_filter_map)
    db.close()
    return filter


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


@st.cache_resource(ttl=3600)
def convert_filter_to_query(filters:Dict[str,List[str]]) -> Query:
    """
    Fetch filtered data from a specified database table based on provided filter conditions.
    """
    global table

    with next(get_db()) as db:
        query = db.query(table)
        for column, values in filters.items():
            if values:
                query = query.filter(table.c[column].in_(values))
    db.close()
    return query

@st.cache_data(ttl=3600)
def convert_selection_to_df(selection: Dict[str,Dict[str,List[str]]]) -> pd.DataFrame:
    """
    Convert a nested dictionary of user selections into a pandas DataFrame by applying the 
    corresponding filters and executing the query.
    """
    filters = convert_selection_to_filter(selection=selection)
    query_w_filter = convert_filter_to_query(filters=filters)
    
    return convert_query_to_df(query_w_filter)

@st.cache_resource(ttl=3600)
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
        editable=True, 
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
    
    # def is_nan(value):
    #     return isinstance(value, float) and math.isnan(value)

    # nans = list(filter(is_nan, input_list))
    # non_nans = list(filter(lambda x: not is_nan(x), input_list))
    # unique_non_nans = list(set(non_nans))
    # if nans:
    #     unique_non_nans.append(float('nan'))
    # return unique_non_nans


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
    
    labels = list(data.keys())
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
