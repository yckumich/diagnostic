import streamlit as st
from data.database import engine, Base
from utils.utils import *
import pandas as pd
from typing import Dict
from st_aggrid import AgGrid, GridUpdateMode, AgGridTheme
from utils.center_tabs import cetner_tab_dict
from utils.utils_center_tab import *
from style import get_style_markdown


# Create the database tables (if they don't already exist)
Base.metadata.create_all(bind=engine)
agg_filter_selection = dict()

#------------------------------HELPER------------------------------
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
        st.markdown("""<div style="height:0px;"></div>""", unsafe_allow_html=True)
        st.divider()  
        st.header('Main-Filters')
        
        for main_filter in filter_map:
            agg_filter_selection[main_filter] = create_filter_expander(main_filter, filter_map[main_filter])

        st.divider()  
        st.header('Current Filter Selection')

        with st.expander("Current Filter Selection"):
            st.json(agg_filter_selection)    
        
    return agg_filter_selection


def display_test_details(test_details):
    for key, value in test_details.items():
        st.write(f"**{key}**: {value}")

#------------------------------MAIN------------------------------
def main():

    st.set_page_config(
        page_title="EDL Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    get_style_markdown()

    #--------------Configure the Main filter--------------
    filter_map = get_filter()
    selection = add_sidebar(filter_map=filter_map)
    #-----------------------------------------------------

    #--------------Configure center pane------------------
    center_tab_col, test_list_col = st.columns([0.86, 0.14], gap="medium")
    

    #--------------Configure Test List--------------------
    with test_list_col:
        st.divider()  
        st.header("Test Names")
        selected_test_df = convert_selection_to_df(selection)
        unique_test_df = (
            selected_test_df[['testname']]
            .drop_duplicates(subset=['testname'])
            .reset_index(drop=True)
            .sort_values(by='testname')
        )
        grid_option = build_grid_option(unique_test_df)
        grid_table = AgGrid(
            data=unique_test_df,
            gridOptions=grid_option,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            height=1000,
            theme=AgGridTheme.MATERIAL
        )

    #--------------Configure Center Tab--------------------
    collected_dataframes = list()
    with center_tab_col:
        
        st.divider()  
        st.header('Tabs')
        st.markdown("""<div style="height:0px;"></div>""", unsafe_allow_html=True)

        # If user selected specfic test/tests in the left panel, refine the selected selected_test_df
        if isinstance(grid_table['selected_rows'], pd.DataFrame):
            sel_row_testname_lst = grid_table['selected_rows']['testname'].to_list()
            selected_test_df = selected_test_df[selected_test_df['testname'].isin(sel_row_testname_lst)]

        tab_titles = list(cetner_tab_dict.keys())
        center_filter_tabs = st.tabs(tab_titles)

        for tab_title, center_filter_tab in zip(tab_titles, center_filter_tabs):
            print(tab_title)
            with center_filter_tab:
                tab_df_titles = cetner_tab_dict[tab_title]
                print(f'\t{tab_df_titles}')
                collected_dataframes.extend(generate_tab_content(tab_title, tab_df_titles, selected_test_df))

    #---------Main Filter Addition for download------------
    with st.sidebar:        
        st.divider()  
        st.header('Download Current Tables')

        if st.button('Download'):
            # for a,b in collected_dataframes:
            #     st.write(a)
            #     st.write(b.shape)
            #     st.write('   ')
            zip_buffer = collect_and_generate_zip(collected_dataframes)
            st.download_button(
                label="Download ZIP",
                data=zip_buffer,
                file_name="dataframes.zip",
                mime="application/zip"
            )
if __name__ == "__main__":
    main()