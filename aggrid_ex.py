from st_aggrid import AgGrid, GridUpdateMode, AgGridTheme
import streamlit as st
import pandas as pd
from st_aggrid.grid_options_builder import GridOptionsBuilder

df = pd.read_csv('https://raw.githubusercontent.com/fivethirtyeight/data/master/airline-safety/airline-safety.csv')
st.dataframe(df)

gd = GridOptionsBuilder.from_dataframe(df)
gd.configure_pagination(enabled=True,paginationPageSize=15, paginationAutoPageSize=False)
gd.configure_default_column(editable=True, groupable=True)

sel_mode = st.radio("Selection Type", options=['single', 'multiple'])

gd.configure_selection(selection_mode=sel_mode, use_checkbox=False)
gridOptions = gd.build()

grid_table = AgGrid(df, gridOptions=gridOptions, update_mode=GridUpdateMode.SELECTION_CHANGED, height=500, theme=AgGridTheme.MATERIAL)
sel_row = grid_table['selected_rows']
st.write(sel_row)
print(sel_row)
print(type(sel_row))