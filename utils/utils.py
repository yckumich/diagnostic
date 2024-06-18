from sqlalchemy.orm.query import Query
from sqlalchemy.orm import Session
from data.database import engine
from data.models import t_tableau3_t2_tjfs_join_edl_dashadmin
from utils.filter import high_level_filter_map
from typing import Dict, List
import streamlit as st
import pandas as pd

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
        unique_values[sub_filter] = list(df[column].unique())
        
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

# @st.cache(allow_output_mutation=True)
def get_filter():
    """
    Retrieves a comprehensive filter dictionary from the database query results.
    """
    db = Session(bind=engine)
    query = db.query(t_tableau3_t2_tjfs_join_edl_dashadmin)
    df = convert_query_to_df(query, None)
    filter = create_filter_map(df, high_level_filter_map)
    del df
    db.close()
    return filter
