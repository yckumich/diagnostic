import streamlit as st
from sqlalchemy.orm import Session
from data.database import engine, Base
from data.models import t_tableau3_t2_tjfs_join_edl_dashadmin
from utils.utils import *
import pandas as pd
from typing import Dict
from st_aggrid import AgGrid, GridUpdateMode, AgGridTheme
from st_aggrid.grid_options_builder import GridOptionsBuilder



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
    
    return agg_filter_selection


def display_test_details(test_details):
    for key, value in test_details.items():
        st.write(f"**{key}**: {value}")


def main():
    st.set_page_config(
        page_title="EDL Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    filter_map = get_filter()
    selection = add_sidebar(filter_map=filter_map)
    selected_test_df = convert_selection_to_df(selection)
    unique_test_df = (selected_test_df[['testname']]
                      .drop_duplicates(subset=['testname'])
                      .reset_index(drop=True)
                      .sort_values(by='testname'))

    test_list_col, test_detail_col = st.columns([0.2, 0.8], gap="small")
    
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
                test_name_list = list(sel_row['testname'])

                if len(test_name_list) == 1 :
                    test_df = selected_test_df[selected_test_df['testname'] == test_name_list[0]]
                    test_detail = create_test_detail(test_df)
                    for detail_title, details in test_detail.items():
                        create_detail_expander(detail_title, details)
                else:
                    pass
            #         print(test_name_list)

            # lst = ['a', 'b', 'c']
            # s = ''
            # for i in lst:
            #     s += "- " + i + "\n"
            # st.markdown(s)

                        

        # if sel_row:
        #     st.dataframe(sel_row)

 
     #.drop_duplicates(subset=['testname']).reset_index(drop=True).sort_values(by='testname')
    # st.dataframe(test_df)

    # # If no test is selected, initialize session state
    # if 'selected_test' not in st.session_state:
    #     st.session_state['selected_test'] = None
    
    # # Layout with two columns
    # test_name_col, test_detail_col = st.columns([0.3, 0.7], gap="small")
    
    # # Display test names in col1
    # with test_name_col:
    #     st.header("Test Names")
    #     AgGrid(test_df[['testname']])


    # print(st.session_state['selected_test'])
    # Display test details in col2 if a test is selected
    # with col2:
    #     if st.session_state['selected_test']:
    #         st.header(f"Details for {st.session_state['selected_test']['testname']}")
    #         display_test_details(st.session_state['selected_test'])
    #     else:
    #         st.write("Select a test to see details.")


if __name__ == "__main__":
    main()