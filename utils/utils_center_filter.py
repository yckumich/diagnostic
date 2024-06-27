import pandas as pd
import streamlit as st

def get_test_by_condition_test_by_condition(df):
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


def get_lab_specific_test_by_laboratory_section(df):
    df = df[[
            'laboratory',
            'testname',
            'test_name_short',
            'test_name_pretty',
            'test_format',
            'test_format_lancet_tier',
        ]].copy()
    df.rename(
        columns={
            'laboratory': 'Laboratory',
            'testname': 'Test Name',
            'test_name_short': 'Test Name Short',
            'test_name_pretty': 'Test Name Pretty',
            'test_format': 'Test Format',
            'test_format_lancet_tier': 'Test Format Lancet Tier',
        },
        inplace=True,
    )
    df = df.drop_duplicates().sort_values(by=list(df.columns)).reset_index(drop=True)
    return df


def get_lab_specific_format_by_test(df):
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


def get_lab_specific_format_and_tiers(df):
    df = df[[
            'test_format',
            'test_format_lancet_tier',
        ]].copy()
    df.rename(
        columns={
            'test_format': 'Test Format',
            'test_name_short': 'Test Name Short',
            'test_format_lancet_tier': 'Test Format Lancet Tier',
        },
        inplace=True,
    )
    df = df.drop_duplicates().sort_values(by=list(df.columns)).reset_index(drop=True)
    return df



def get_test_by_medicine_test_by_medicine(df):
    """
    Medicine
    Test
    Test Reason
    Test Note
    Med/Cond Note
    """
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
    return df

def get_test_by_med_and_cond_test_by_medicine_and_condition(df):
    df = df.drop_duplicates().sort_values(by=list(df.columns)).reset_index(drop=True)
    return df

def get_test_tests(df):
    df = df.drop_duplicates().sort_values(by=list(df.columns)).reset_index(drop=True)
    return df

def get_condition_by_test_conditions_per_test(df):
    df = df.drop_duplicates().sort_values(by=list(df.columns)).reset_index(drop=True)
    return df

def get_medicine_indications_medicine_indications(df):
    df = df.drop_duplicates().sort_values(by=list(df.columns)).reset_index(drop=True)
    return df

def get_tests_and_cond_test_lists_by_condition(df):
    df = df.drop_duplicates().sort_values(by=list(df.columns)).reset_index(drop=True)
    return df

def get_test_indication_test_indication(df):
    df = df.drop_duplicates().sort_values(by=list(df.columns)).reset_index(drop=True)
    return df


@st.cache_data(ttl=3600)
def generate_tab_content(tab_title, df_titles, df):

    tab_func_names = [
        "get_" +
        tab_title.replace(" ", "_").lower() + 
        "_" +  
        df_title.replace(" ", "_").lower()
        for df_title in df_titles
    ]

    cols = st.columns(len(tab_func_names))
    for i, (col, tab_func_name) in enumerate(zip(cols, tab_func_names)):
        with col:
            st.markdown(f"<div class='small-title'>{df_titles[i]}</div>", unsafe_allow_html=True)
            result_df = globals()[tab_func_name](df)
            st.markdown(f"<div class='tight-container'>", unsafe_allow_html=True)
            st.dataframe(
                data=result_df, 
                use_container_width=True,
                height=900,
            )