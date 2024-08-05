import pandas as pd
import streamlit as st
import time


@st.cache_data(ttl=3600)
def get_test_by_condition_test_by_condition(df, custom_condition_tier=False, custom_test_tier=False):
    df = df[[
            'conditionname',
            'condition_name_lancet',
            'conditionlevel',
            'test_name_pretty',
            'test_name_short',
            'testreason'
        ]].copy()
    df.rename(
        columns={
            'conditionname': "Condition Name",
            'condition_name_lancet': "Condition Name Lancet",
            'conditionlevel': "Condition Level",
            'test_name_pretty': "Test Name Pretty",
            'test_name_short': "Test Name",
            'testreason': "Test Reason",
        },
        inplace=True,
    )
    df = df.drop_duplicates().sort_values(by=list(df.columns)).reset_index(drop=True)
    return df


def get_lab_specific_test_by_laboratory_section(df, custom_condition_tier=False, custom_test_tier=False):
    if "temp_clstbls_df" not in st.session_state:
        st.session_state.temp_clstbls_df = None

    if "cached_tbls_all_cols" not in st.session_state:
        st.session_state.cached_tbls_all_cols = None
    
    if custom_condition_tier and custom_test_tier:
        st.session_state.cached_tbls_all_cols = df

    columns = [
        'laboratory',
        'testname',
        'test_name_short',
        'test_name_pretty',
        'test_format',
        'test_format_lancet_tier',
        'lancet_condition_tier',
    ]
    rename_map = {
        'laboratory': 'Laboratory',
        'testname': 'Test Name',
        'test_name_short': 'Test Name Short',
        'test_name_pretty': 'Test Name Pretty',
        'test_format': 'Test Format',
        'test_format_lancet_tier': 'Test Format Lancet Tier',
        'lancet_condition_tier': 'Lancet Condition Tier'
    }

    if custom_test_tier:
        columns.append('custom_test_tier')
        rename_map['custom_test_tier'] = 'Test Format Custom Tier'
        
    if custom_condition_tier:
        columns.append('custom_condition_tier')
        rename_map['custom_condition_tier'] = 'Custom Condition Tier'

    df = df[columns].copy()

    df.rename(
        columns=rename_map,
        inplace=True,
    )
    df = df.drop_duplicates().dropna().sort_values(by=list(df.columns)).reset_index(drop=True)
    
    custom_col_list = []
    for col in ['Custom Condition Tier','Test Format Custom Tier']:
        if col in df.columns:
            custom_col_list.append(col)

    def apply_color(_):
        return f"background-color: lightblue;"

    df = df.style.map(apply_color, subset=custom_col_list)

    if len(custom_col_list) ==  2:
        st.session_state.temp_clstbls_df = df.data

    return df

@st.cache_data(ttl=3600)
def get_lab_specific_format_by_test(df, custom_condition_tier=False, custom_test_tier=False):
    df = df[[
            'test_name_pretty',
            'test_name_short',
            'test_format',
        ]].copy()
    
    df.rename(
        columns={
            'test_name_pretty': 'Test Name Pretty',
            'test_name_short': 'Test Name Short',
            'test_format': 'Test Format',
        },
        inplace=True,
    )
    df = df.drop_duplicates().sort_values(by=list(df.columns)).reset_index(drop=True)
    return df

@st.cache_data(ttl=3600)
def get_lab_specific_format_and_tiers(df, custom_condition_tier=False, custom_test_tier=False):
    columns = [
        'test_format',
        'test_format_lancet_tier',
    ]
    rename_map = {
        'test_format': 'Test Format',
        'test_name_short': 'Test Name Short',
        'test_format_lancet_tier': 'Test Format Lancet Tier',
    }
    
    if custom_test_tier:
        columns.append('custom_test_tier')
        rename_map['custom_test_tier'] = 'Custom Test Tier'


    df = df[columns].copy()
    df.rename(
        columns=rename_map,
        inplace=True,
    )
    df = df.drop_duplicates().sort_values(by=list(df.columns)).reset_index(drop=True)
    return df


@st.cache_data(ttl=3600)
def get_test_by_medicine_test_by_medicine(df, custom_condition_tier=False, custom_test_tier=False):

    df = df[[
            'medicine',
            'test_name_short',
            'testreason',
            'testnote',
            'medicineorconditionnote',
        ]].copy()
    df.rename(
        columns={
            'medicine':'Medicine',
            'test_name_short':'Test',
            'testreason':'Test Reason',
            'testnote':'Test Note',
            'medicineorconditionnote':'Med/Cond Note',
        },
        inplace=True,
    )
    df = df.drop_duplicates().sort_values(by=list(df.columns)).reset_index(drop=True)
    return df.head()


@st.cache_data(ttl=3600)
def get_test_by_med_and_cond_test_by_medicine_and_condition(df, custom_condition_tier=False, custom_test_tier=False):
    df = df.drop_duplicates().sort_values(by=list(df.columns)).reset_index(drop=True)
    return df.head()


@st.cache_data(ttl=3600)
def get_test_tests(df, custom_condition_tier=False, custom_test_tier=False):
    df = df.drop_duplicates().sort_values(by=list(df.columns)).reset_index(drop=True)
    return df.head()


@st.cache_data(ttl=3600)
def get_condition_by_test_conditions_per_test(df, custom_condition_tier=False, custom_test_tier=False):
    df = df.drop_duplicates().sort_values(by=list(df.columns)).reset_index(drop=True)
    return df.head()


@st.cache_data(ttl=3600)
def get_medicine_indications_medicine_indications(df, custom_condition_tier=False, custom_test_tier=False):
    df = df.drop_duplicates().sort_values(by=list(df.columns)).reset_index(drop=True)
    return df.head()


@st.cache_data(ttl=3600)
def get_tests_and_cond_test_lists_by_condition(df, custom_condition_tier=False, custom_test_tier=False):
    df = df.drop_duplicates().sort_values(by=list(df.columns)).reset_index(drop=True)
    return df.head()


@st.cache_data(ttl=3600)
def get_test_indication_test_indication(df, custom_condition_tier=False, custom_test_tier=False):
    df = df.drop_duplicates().sort_values(by=list(df.columns)).reset_index(drop=True)
    return df.head()


# @st.cache_data(ttl=3600)
def generate_tab_content(tab_title, 
                         df_titles, 
                         df, 
                         custom_condition_tier_df=None,
                         custom_test_tier_df=None):

    tab_dataframes = list()

    tab_func_names = [
        "get_" +
        tab_title.replace(" ", "_").lower() + 
        "_" +  
        df_title.replace(" ", "_").lower()
        for df_title in df_titles
    ]
    ## APPLY BROADCASTING--CONDITION TIER
    condition_tier_exist = isinstance(custom_condition_tier_df, pd.DataFrame)
    if condition_tier_exist:
        df = pd.merge(
            left=df, right=custom_condition_tier_df[['conditionname', 'conditionlevel', 'custom_condition_tier']], 
            on=['conditionname', 'conditionlevel'],
            how='left',
        )
    ## APPLY BROADCASTING--TEST TIER
    test_tier_exist = isinstance(custom_test_tier_df, pd.DataFrame)
    if test_tier_exist:
        df = pd.merge(
            left=df, right=custom_test_tier_df[['test_format', 'custom_test_tier']], 
            on=['test_format',],
            how='left',
        )

    cols = st.columns(len(tab_func_names))
    for i, (col, tab_func_name) in enumerate(zip(cols, tab_func_names)):
        with col:
            st.markdown(f"<div class='small-title'>{df_titles[i]}</div>", unsafe_allow_html=True)
            
            result_df = globals()[tab_func_name](
                df, 
                custom_condition_tier=condition_tier_exist,
                custom_test_tier=test_tier_exist
            )
            
            st.markdown(f"<div class='tight-container'>", unsafe_allow_html=True)
            st.dataframe(
                data=result_df, 
                use_container_width=True,
                height=900,
            )
        if (df_titles[i] == 'Test By Laboratory Section') and ('Custom Condition Tier' in result_df.columns)  and  ('Custom Condition Tier' in result_df.columns):
            if st.button("Save Current 'Test By Laboratory Section' Table"):
                st.session_state.temp_clstbls_df = result_df.data
                msg = st.toast("Saving current 'Test By Laboratory' table...")
                time.sleep(0.7)
                msg.toast('Saved ✅')
                time.sleep(0.7)
                st.rerun()

        tab_dataframes.append((df_titles[i], result_df))
    return tab_dataframes
