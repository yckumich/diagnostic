import streamlit as st
import pandas as pd 
import numpy as np
import warnings
warnings.filterwarnings("ignore")

# def get_view_df(
#             loc="static/tableau3_t2_tjfs_join_edl_dashadmin.csv",
#             drop_cols=['indonesia_phc_exclude','ghana_nhis_reimbursement_usd'],
#             ):
#       view_df = pd.read_csv(loc).drop(columns=drop_cols, errors='ignore')
#       view_df = view_df.fillna(np.nan).replace([np.nan], [None])

def get_view_df():
      view_df = pd.read_csv("static/tableau3_t2_tjfs_join_edl_dashadmin.csv").fillna(np.nan).replace([np.nan], [None])

      if (('custom_condition_df' in st.session_state) and 
            (isinstance(st.session_state['custom_condition_df'], pd.DataFrame)) and
            (st.session_state['custom_condition_df'].shape[0] > 0)):
            # print('custom_condition_df EXIST!')
            # print('Before merge: ',view_df.shape)
            view_df = (
                  pd.merge(
                        left=view_df, 
                        right=st.session_state.custom_condition_df[
                              [
                                    'conditionname', 
                                    'conditionlevel',
                                    # 'custom_condition_tier'
                              ]
                        ], 
                        on=['conditionname', 'conditionlevel'],
                        how='inner',
                  )
                  # .dropna(subset=['custom_condition_tier'], axis=0)
                  # .drop(columns=['custom_condition_tier'])
                  .reset_index(drop=True)
            )
            # print('After merge: ',view_df.shape)
            # print("  ")

      if (('custom_test_tier_df' in st.session_state) and 
            (isinstance(st.session_state['custom_test_tier_df'], pd.DataFrame)) and
            (st.session_state['custom_test_tier_df'].shape[0] > 0)):
            # print('custom_test_tier_df EXIST!')
            # print('Before merge: ',view_df.shape)
            view_df = (
                  pd.merge(
                        left=view_df, 
                        right=st.session_state.custom_test_tier_df[
                              [
                                    'test_format',
                                    # 'custom_test_tier'
                              ]
                        ], 
                        on=['test_format',],
                        how='inner',
                        )
                  # .dropna(subset=['custom_test_tier'], axis=0)
                  # .drop(columns=['custom_test_tier'])
                  .reset_index(drop=True)
            )
            # print('After merge: ',view_df.shape)
            # print("  ")
      # print("returning view_df: ", view_df.shape)
      return view_df