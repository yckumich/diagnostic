import streamlit as st
import pandas as pd 
import numpy as np

@st.cache_resource(ttl=7200)
def get_view_df(loc="static/tableau3_t2_tjfs_join_edl_dashadmin.csv",
                drop_cols=[
                  'indonesia_phc_exclude',
                  'ghana_nhis_reimbursement_usd'
              ]):
    view_df = pd.read_csv(loc).drop(columns=drop_cols, errors='ignore')
    view_df = view_df.fillna(np.nan).replace([np.nan], [None])
    
    return view_df

view_df = get_view_df()