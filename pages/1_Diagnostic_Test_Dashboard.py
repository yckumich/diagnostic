import streamlit as st

## PAGE CONFIG
st.set_page_config(
    page_title="EDL Dashboard",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.logo(image="static/CGHE_formal_horizontal.png",
        icon_image="static/CGHE_formal_horizontal.png",
        size="large")

import time
import pandas as pd
from typing import Dict, List
from st_aggrid import AgGrid, GridUpdateMode, AgGridTheme
from utils.dataframe_utils.center_tabs import centner_tab_dict
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

if 'selected_test_names' not in st.session_state:
    st.session_state['selected_test_names'] = []

for _subfilter_map in high_level_filter_map.values():
    for _subfilter_title in _subfilter_map:
        if _subfilter_title not in st.session_state:
            st.session_state[_subfilter_title] = []



# ---------- SAFE RESET (per-table) ------------------------------
# If either list is empty, clear **only** its paired DataFrame.
# Also clear the cached snapshot if either list is missing.
if not st.session_state.custom_condition_list:
    st.session_state.custom_condition_df = None
if not st.session_state.custom_test_tier_list:
    st.session_state.custom_test_tier_df = None

if (not st.session_state.custom_condition_list) or (
    not st.session_state.custom_test_tier_list
):
    st.session_state.cached_tbls_all_cols = None
# ---------------------------------------------------------------


agg_filter_selection = dict()

#------------------------------HELPERS------------------------------
def create_filter_expander(expander_title:str, subfilter_map:dict) -> Dict:
    selected_option_map = {k:[] for k in subfilter_map.keys()}
    with st.expander(expander_title, expanded=False):

        for subfilter_title, options_list in subfilter_map.items():
            selected_option_map[subfilter_title] = st.multiselect(
                subfilter_title,
                options_list,
                key=subfilter_title
            )
    return selected_option_map


def create_detail_expander(detail_title:str, details:List):
    if detail_title != 'testname':
        with st.expander("**"+detail_title+"**"):
            markdown_string = ''
            for detail in details:
                markdown_string += "- " + str(detail) + "\n"
            st.markdown(markdown_string)


def clear_all_filters(filter_map):
    for subfilter_map in filter_map.values():
        for subfilter_title in subfilter_map:
            if subfilter_title in st.session_state:
                st.session_state[subfilter_title] = []


def add_sidebar(filter_map):
    with st.sidebar:
        st.markdown("""<div style="height:0px;"></div>""", unsafe_allow_html=True)

        st.header('Filter')

        for main_filter in filter_map:
            agg_filter_selection[main_filter] = create_filter_expander(main_filter, filter_map[main_filter])

        tiers_ok = bool(st.session_state.get('custom_condition_list')) and bool(
            st.session_state.get('custom_test_tier_list')
        )
        save_btn_disabled = not tiers_ok

        save_col, clear_col = st.columns(2)
        with save_col:
            if st.button("Save Filter", disabled=save_btn_disabled, key="save_filter_state"):
                msg = st.toast("Saving current filter state…")
                time.sleep(0.7)
                msg.toast("Saved ✅")
        with clear_col:
            st.button("Clear Filter", on_click=clear_all_filters, args=(filter_map,))

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
#--------------Configure center pane------------------
center_tab_col, test_list_col = st.columns([0.8, 0.2], gap="medium")

#--------------Configure Test List--------------------
with test_list_col:
    st.markdown("""<div style="height:72px;"></div>""", unsafe_allow_html=True)
    st.divider()
    # st.header("Test Name")
    st.markdown(
        "<h2 style='font-size:2rem;'>Test Name</h2>",
        unsafe_allow_html=True
    )

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
    cond_badge, test_badge = st.columns(2)

    with cond_badge:
        if st.session_state.custom_condition_list:
            st.success("Custom Condition Tier Applied ✅")
        else:
            st.warning("Custom Condition Tier Not Applied 🚨")

    with test_badge:
        if st.session_state.custom_test_tier_list:
            st.success("Custom Test-Format Tier Applied ✅")
        else:
            st.warning("Custom Test-Format Tier Not Applied 🚨")

    st.divider()
    st.header('Tabs')
    st.markdown("""<div style="height:0px;"></div>""", unsafe_allow_html=True)

    # If user selected specific test/tests in the left panel, refine the selected selected_test_df
    if isinstance(grid_table['selected_rows'], pd.DataFrame) and not grid_table['selected_rows'].empty:
        st.session_state['selected_test_names'] = grid_table['selected_rows']['testname'].to_list()
    elif not isinstance(grid_table['selected_rows'], pd.DataFrame):
        st.session_state['selected_test_names'] = []

    if st.session_state['selected_test_names']:
        selected_test_df = selected_test_df[selected_test_df['testname'].isin(st.session_state['selected_test_names'])]
        # print(selected_test_df.shape)
    tab_titles = list(centner_tab_dict.keys())
    center_filter_tabs = st.tabs(tab_titles)
    for tab_title, center_filter_tab in zip(tab_titles, center_filter_tabs):
        with center_filter_tab:
            tab_df_titles = centner_tab_dict[tab_title]
            collected_dataframes.extend(generate_tab_content(
                tab_title,
                tab_df_titles,
                selected_test_df,
                st.session_state.custom_condition_df if custom_condition_df_exist else None,
                st.session_state.custom_test_tier_df if custom_test_tier_df_exist else None
            ))