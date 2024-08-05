import streamlit as st
import pandas as pd 
import numpy as np
import warnings
warnings.filterwarnings("ignore")

if 'merge_custom_condition' not in st.session_state:
      st.session_state['merge_custom_condition'] = False

if 'merge_custom_test' not in st.session_state:
      st.session_state['merge_custom_test'] = False

# @st.cache_resource(ttl=3600)
def get_view_df(
            loc="static/tableau3_t2_tjfs_join_edl_dashadmin.csv",
            drop_cols=['indonesia_phc_exclude','ghana_nhis_reimbursement_usd'],
            # merge_custom_condition=st.session_state.merge_custom_condition,
            # merge_custom_test=st.session_state.merge_custom_test
            ):
      
      print(f"*********Inside get_view_df*********")

      view_df = pd.read_csv(loc).drop(columns=drop_cols, errors='ignore')
      view_df = view_df.fillna(np.nan).replace([np.nan], [None])

      # if merge_custom_condition:
      if (('custom_condition_df' in st.session_state) and 
            (isinstance(st.session_state['custom_condition_df'], pd.DataFrame)) and
            (st.session_state['custom_condition_df'].shape[0] > 0)):
            print('EXIST: custom_condition_df')
            view_df = (
                  pd.merge(
                        left=view_df, 
                        right=st.session_state.custom_condition_df [
                              ['conditionname', 
                              'conditionlevel',
                              'custom_condition_tier']
                        ], 
                        on=['conditionname', 'conditionlevel'],
                        how='left',
                  )
                  .dropna(subset=['custom_condition_tier'], axis=0)
                  .drop(columns=['custom_condition_tier'])
                  .reset_index(drop=True)
            )
      else:
            print('NOT EXIST: custom_condition_df')
      # st.session_state.merge_custom_condition = False
      # if merge_custom_test:
      if (('custom_test_tier_df' in st.session_state) and 
            (isinstance(st.session_state['custom_test_tier_df'], pd.DataFrame)) and
            (st.session_state['custom_test_tier_df'].shape[0] > 0)):
            print('EXIST: custom_test_tier_df')
            view_df = (
                  pd.merge(
                        left=view_df, 
                        right=st.session_state.custom_test_tier_df [
                              ['test_format',
                              'custom_test_tier']
                        ], 
                        on=['test_format',],
                        how='left',
                        )
                  .dropna(subset=['custom_test_tier'], axis=0)
                  .drop(columns=['custom_test_tier'])
                  .reset_index(drop=True)
            )
      else:
            print('NOT EXIST: custom_test_tier_df')
      # st.session_state.merge_custom_test = False
      if 'view_df' not in st.session_state:
         st.session_state['view_df'] = None

      st.session_state['view_df'] = view_df

      # print(st.session_state['view_df'].shape)
      # print(" ")
      print(f"view_df.shape: {view_df.shape}")
      # print(f"merge_custom_condition: {merge_custom_condition}")
      # print(f"merge_custom_test: {merge_custom_test}")
      print("  ")


      return st.session_state['view_df']