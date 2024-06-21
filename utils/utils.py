from sqlalchemy.orm.query import Query
from sqlalchemy.sql.schema import Table
from sqlalchemy.orm import Session

from data.database import engine
from data.models import t_tableau3_t2_tjfs_join_edl_dashadmin as table

from utils.filter import high_level_filter_map
from typing import Dict, List, Any

import streamlit as st
import pandas as pd
import math

from st_aggrid import AgGrid, GridUpdateMode, AgGridTheme
from st_aggrid.grid_options_builder import GridOptionsBuilder



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

    db = Session(bind=engine)
    query = db.query(table)
    df = convert_query_to_df(query, None)
    filter = create_filter_map(df, high_level_filter_map)
    del df
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

    db = Session(bind=engine)
    query = db.query(table)
    
    for column, values in filters.items():
        if values:
            query = query.filter(table.c[column].in_(values))
    
    return query

@st.cache_data(ttl=3600)
def convert_selection_to_df(selection: Dict[str,Dict[str,List[str]]]) -> pd.DataFrame:
    """
    Convert a nested dictionary of user selections into a pandas DataFrame by applying the 
    corresponding filters and executing the query.
    """
    print("RUNNING: convert_selection_to_df")
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
        use_checkbox=True
    )
    return gd.build()

@st.cache_data(ttl=3600)
def get_unique_values(input_list: List[Any]) -> List[Any]:
    """
    This function takes a list containing various types including float('nan') and returns a new list
    with unique values and compresses all 'nan' values into a single occurrence.
    """
    def is_nan(value):
        return isinstance(value, float) and math.isnan(value)

    nans = list(filter(is_nan, input_list))
    non_nans = list(filter(lambda x: not is_nan(x), input_list))
    unique_non_nans = list(set(non_nans))
    if nans:
        unique_non_nans.append(float('nan'))
    return unique_non_nans

@st.cache_data(ttl=3600)
def create_test_detail(df:pd.DataFrame):
    """
    df contains dataframe of a single test
    """
    col_to_unique_map = dict()
    for col in df.columns:
        col_to_unique_map[col] = get_unique_values(list(df[col]))
    
    return col_to_unique_map
        