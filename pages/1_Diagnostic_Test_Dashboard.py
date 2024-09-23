import streamlit as st

## PAGE CONFIG
st.set_page_config(
    page_title="EDL Dashboard",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

UM_Block_Logo = "static/Block_M-Hex.png"
UM_Extended_Logo = "static/U-M_Logo-Horizontal-Hex.png"

st.logo(UM_Extended_Logo, icon_image=UM_Block_Logo)

import pandas as pd
from typing import Dict, List
from st_aggrid import AgGrid, GridUpdateMode, AgGridTheme
from utils.dataframe_utils.center_tabs import cetner_tab_dict
from utils.dataframe_utils.utils_center_tab import *
from utils.dataframe_utils.utils import *
from style import get_style_markdown

#------------------------------INIT------------------------------

## SESSION STATE
if "custom_condition_list" not in st.session_state:
    st.session_state.custom_condition_list = []

if "custom_condition_df" not in st.session_state:
    st.session_state.custom_condition_df = None

if 'show_plot' not in st.session_state:
    st.session_state['show_plot'] = False

if "custom_test_tier_list" not in st.session_state:
    st.session_state.custom_test_tier_list = []

if "custom_test_tier_df" not in st.session_state:
    st.session_state.custom_test_tier_df = None

if 'show_test_tier_plot' not in st.session_state:
    st.session_state['show_test_tier_plot'] = False

agg_filter_selection = dict()

#------------------------------HELPERS------------------------------
def create_filter_expander(expander_title:str, subfilter_map:dict) -> Dict:
    selected_option_map = {k:[] for k in subfilter_map.keys()}
    with st.expander(expander_title, expanded=True if expander_title=='Diagnostic' else False):

        for subfilter_title, options_list in subfilter_map.items():
            selected_option_map[subfilter_title] = st.multiselect(
                subfilter_title, 
                options_list, 
                # default=['Blood bank', ] if subfilter_title == 'Laboratory' else [],
                default=[]
            )
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

        st.header('Filter')

        for main_filter in filter_map:
            agg_filter_selection[main_filter] = create_filter_expander(main_filter, filter_map[main_filter])

        st.divider()
        st.header('Current Filter Selection')

        with st.expander("Current Filter Selection"):
            st.json(agg_filter_selection)

        st.divider()
        st.markdown(sidebar_instruction)
    return agg_filter_selection

#------------------------------MAIN------------------------------
get_style_markdown()

#--------------Configure the Main filter--------------
filter_map = get_filter()
selection = add_sidebar(filter_map=filter_map)
# print(selection)
#--------------Configure center pane------------------
center_tab_col, test_list_col = st.columns([0.86, 0.14], gap="medium")

#--------------Configure Test List--------------------
with test_list_col:
    st.markdown("""<div style="height:72px;"></div>""", unsafe_allow_html=True)
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
    # print(selected_test_df.shape)
    grid_table = AgGrid(
        data=unique_test_df,
        gridOptions=grid_option,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        height=1000,
        theme=AgGridTheme.MATERIAL
    )

#--------------Configure Center Tab--------------------
collected_dataframes = list()
custom_condition_df_exist = isinstance(st.session_state.custom_condition_df, pd.DataFrame)
custom_test_tier_df_exist = isinstance(st.session_state.custom_test_tier_df, pd.DataFrame)

with center_tab_col:
    condition_tier_col, test_tier_col = st.columns([0.5, 0.5])
    with condition_tier_col:
        if custom_condition_df_exist:
            st.success('Custom Condition Tier Applied ✅')
        else:
            st.warning('Custom Condition Tier Not Applied 🚨')
    with test_tier_col:
        if custom_test_tier_df_exist:
            st.success('Custom Test-Format Tier Applied ✅')
        else:
            st.warning('Custom Test-Format Tier Not Applied 🚨')

    st.divider()
    st.header('Tabs')
    st.markdown("""<div style="height:0px;"></div>""", unsafe_allow_html=True)

    # If user selected specfic test/tests in the left panel, refine the selected selected_test_df
    if isinstance(grid_table['selected_rows'], pd.DataFrame):
        sel_row_testname_lst = grid_table['selected_rows']['testname'].to_list()
        selected_test_df = selected_test_df[selected_test_df['testname'].isin(sel_row_testname_lst)]
        # print(selected_test_df.shape)
    tab_titles = list(cetner_tab_dict.keys())
    center_filter_tabs = st.tabs(tab_titles)
    for tab_title, center_filter_tab in zip(tab_titles, center_filter_tabs):
        with center_filter_tab:
            tab_df_titles = cetner_tab_dict[tab_title]
            collected_dataframes.extend(generate_tab_content(
                tab_title,
                tab_df_titles,
                selected_test_df,
                st.session_state.custom_condition_df if custom_condition_df_exist else None,
                st.session_state.custom_test_tier_df if custom_test_tier_df_exist else None
            ))

#---------Main Filter Addition for download------------
# with st.sidebar:
#     st.divider()
#     st.header('Download Current Tables')

#     if st.button('Download'):
#         zip_buffer = collect_and_generate_zip(collected_dataframes)
#         st.download_button(
#             label="Download ZIP",
#             data=zip_buffer,
#             file_name="dataframes.zip",
#             mime="application/zip"
#         )
